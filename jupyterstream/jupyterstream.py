import os
import warnings
from subprocess import call

class JupyterStream():
    """

    Parameters
    ----------
    run : bool
        True - execute
        False - do not execute (i.e a useful safty to examine the call before running)

    verbose : bool
        increase output verbosity
    """
    
    def __init__(self, run=False, verbose=True):
        self.run = run
        self.verbose = verbose
        
    def runipy_wrapper(self, val, val_name="val", notebook_origin= None, notebook_prefix= None, notebook_dirnew=None):
        """Builds and executes a runipy command line for cloning a Jupyter notebook and running.

        Parameters
        ----------
        val : str
            The variable to be passed to the notebook

        val_name : str
            The variable name, as appears in the notebook
            
        notebook_origin : str
            The original notebook to be clones, e.g "/my/path/my_notebook.ipynb"
            
        notebook_prefix: str
            Notebook name, without postfix `ipynb` or path, e.g "my_notebook"
            
        notebook_dirnew: str
            Path for new notebook, e.g "/my/path/notebook_runs/"

        """
        
        # verifying existance of the outdir
        if not os.path.exists(notebook_dirnew):
            os.makedirs(notebook_dirnew)
            
        # creating the new notebook
        notebook_new = "{}{}_{}.ipynb".format(notebook_dirnew, notebook_prefix, val)
        
        if self.run:
            print "Creating {}".format(notebook_new)
            os.system("cp %s %s"%(notebook_origin, notebook_new)) 
        

        # creating the bash line command (for display)
        str_command = "{}={} runipy -o {}".format(val_name, val, notebook_new)
        print "=================================================="
        print str_command
        print "=================================================="

        # execution
        if self.run:
            os.environ[val_name] = val
            call(["runipy","-o", notebook_new])
        else:
            if self.verbose:
                print "(The above is the ruinpy call, but it did not execute.) To execute, add the flag: --run "
        
    def parallel_execute(self, bash_program, list_vals, jobs=None):
        """Builds and executes a parallel command line for cloning a Jupyter notebook and running.

        Parameters
        ----------
        bash_program : str
            The bash program to run. E.g "python demo.py"
            
        list_vals : list
            List of values to be pushed
            
        jobs: str
            N jobs tp run in parallel
            
        """
        
        if not jobs:
            jobs = int(2)
        else:
            try:
                jobs = int(jobs)
            except ValueError:
                warnings.warn("jobs must be an integeter. Setting to jobs=2", DeprecationWarning)
                jobs = int(2)
            
        nvals = len(list_vals) # program = 'python runipy_wrapper.py'
        if self.verbose:
            print list_vals
        print "Number of values: {}".format(nvals)
        
        list_vals_str = " ".join(list_vals)
        nparallel_str = str( min([jobs, nvals]) )

        if self.run:
            bash_program += ' --run'

        command = 'parallel -j {} {} '.format(nparallel_str, bash_program)
        command += '-l '
        command += '{1}'
        command += ' ::: {}'.format(list_vals_str)

        print "=================================================="
        print command
        print "=================================================="

        if self.run:
            os.system(command)
        else:
            if self.verbose:
                print "(The above is the parallel call, but it did not run.) To execute, add the flag: --run "