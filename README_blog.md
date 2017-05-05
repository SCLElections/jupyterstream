# Data Deadline?  Jupyter to the Rescue!

**Python data delivery streamlines simplified by handy manipulations of Jupyter notebooks**

After completing the exploratory phase on a Jupyter notebook, and nearing a deadline, you have a few options to prepare for a quick delivery. The first obvious choice would be to run the notebook with the full data for delivery. Alternatively you could download as a python script and run from the command line.
Before delivering, however, you would probably want to verify that the final distributions and metrics appear reasonable. To receive rapid and interactive feedback, a Jupyter environment would seem the obvious choice. But what if you needed to loop by a keyword?

We suggest using `runipy` to multi-run notebooks. A master notebook would collect the important metrics and figures (!) for analysis once the notebooks have completed. This way you can determine which runs were successful and which require special attention.

In this post we cover and provide [code](https://github.com/cambridgeanalytica/jupyterstream) for:  
* Applying [`runipy`](https://pypi.python.org/pypi/runipy), a convienient tool to run a notebook from the command line
* Using [`nbformat`](https://nbformat.readthedocs.io/en/latest/format_description.html), a python module to read text and image outputs from notebooks.  
* We also briefly discuss parallelising using the bash command `parallel`.   


***Disclaimer:*** *This is not an exhaustive explanation of the functionality of `runipy`, `nbformat` or `parallel`, but rather a suggestion from which you can develop your own preference for use.* 

We demonstrate the usefulness of the above by calculating the distribution of USA voters' Registration Date as a function of time. Our SQL database contains information of all 220 million voters, where each state has its own schema (51, including Washington DC).  

Generic and demo code (and data) is provided on [GitHub](https://github.com/cambridgeanalytica/jupyterstream). Below we refer to `py` scripts and cells within `.ipynb` notebooks, but there is no need to download to follow.

![Alt text](./png/jupyterstream.png?raw=true "Title")  

## `runipy`
`runipy` enables you to run a Jupyter notebook as a script by relying on the notebook's JSON structure. For a full description of it's capabilities and installation, please refer to Paul Butler's [git repository, (thanks Paul!)](https://github.com/paulgb/runipy). Here we focus on a few useful commands.

After installing you will be able to:  
  * Run a notebook from the command line: `runipy notebook.ipynb`
  * Run a notebook from the command line while saving the results in the notebook (overwrite):  `runipy -o notebook.ipynb`   
  * Run a notebook from the command line while saving the results in a new one: `runipy notebook.ipynb notebook_new.ipynb`
  * Run a notebook from the command line while passing an arguement: `myvar=value runipy notebook.ipynb`  
  The argument would be then read in the notebook by `myvar = os.environ['myvar']`

Next, we discuss our method of use: clone a notebook and then execute it.

## A Wrapper for `runipy`
One method to prepare for a multi-notebook-run is creating new notebooks that are similar to the original and feeding them the variable value. This is useful because you can save the results of each execution for later analysis.  

For this purpose we suggest writing a script to:  
  * Clone the original notebook
  * Apply `runipy` on the clone


A python runipy wrapper might look like this:  
```
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
```

The key lines are:
  * `os.system("cp %s %s"%(notebook_origin,notebook_new)) ` Clones the original notebook to the one we want to run.
  * `str_command = "{}={} runipy -o {}".format(str_var, val, notebook_new)` runs the new notebook at the bash line while passing the arguement. (We use this just for display.)
  * `os.environ[val_name] = val` actually passes the argument.
  * `subprocess.call(["runipy","-o", notebook_new])` is the actual execution command (pythonic version of the above). 

  
To demonstrate the use of this function we have prepared a [demo](https://github.com/cambridgeanalytica/jupyterstream/tree/master/demo).  



## Reading notebook information with `nbformat`
So far we've seen how to clone notebooks, pass arguments and execute as a script. We leave it up to the user to figure out the preferred method to run the notebooks (loop or parallel; see the Appendix for our usage of `parallel`), and assume that all notebooks have been completed.  

We now describe how to read and display information from the completed notebooks.   The information and code in this section may also be found this [demo notebook](https://github.com/cambridgeanalytica/jupyterstream/blob/master/demo/notebooks/my_notebook_master.ipynb).

### Reading a notebook

To read from an `.ipynb` file `file_notebook`:
```
import nbformat
notebook_version = 4
notebook = nbformat.read(file_notebook, notebook_version)
```
* `notebook_version` dictates the formatting. For compatibility with the functions below, we set it to version 4. One could alternatively set to other values (1, 2, 3) or leave as is with `notebook_version = nbformat.NO_CONVERT`. See JSON format renaming with the different versions  [here](http://nbformat.readthedocs.io/en/latest/format_description.html?highlight=execution_count).

### Cell Information

To pull information from a cell, one is required to define: 
  * Which `out_value` is of interest?
  * What is the format of the cell: text or image?    
  
  
By `out_value` we are referring to the numerical value in the square brackets in a notebook on the left margin where is says "Out[`out_value`]:".

<img src="blog-runipy/jupyterstream_image_03.png" width="100">

Once `out_value` is determined this script retreives the cell infromation:
```
def select_cell(notebook, out_value):
    """
    returns the information of a cell
    """
    
    # Notebook formatting defintions
    if notebook["nbformat"] < 4:
        cell_all = list(notebook["worksheets"][0]["cells"])
        key_counter = 'prompt_number'
    else:
        cell_all = list(notebook["cells"])
        key_counter = 'execution_count'
    
    # Finding and returning the relevant cell
    for icell, cell in enumerate(cell_all):
        try: # Not all Cells have the `key_counts`
            if cell[key_counter] == out_value:
                return cell
        except:
            None
            
    return None
```
* The `if notebook["nbformat"] < 4` condition verifies that the cell yields the correct dictionary formatting
* The `for icell, cell in enumerate(cell_all):` loop searches for the relevant cell and return it once it is found.

### Cell Information Formatting
Now that we have the cell information let's dispaly it.

**Text**  
This function will extract the text (assuming version 4):  
```
def cell_text(cell, item_value):
    return cell["outputs"][item_value]["data"]["text/plain"]
```
* `item_value`: As `cell["outputs"]` is a list of possible combinations (text and image, more than one image, etc.), one must define which item to display.

Specifics on how to display the text highly depends on how the text was constructed. In our ([demo notebook](https://github.com/cambridgeanalytica/public/blob/master/jupyterstream/notebooks/my_notebook_master.ipynb)  ) we show how to dispaly DataFrame information and its limitations (see the function `cell2df`).

**Images**

This function will extract a string of an image (either version 4 or prior)  
```
def cell_to_image(cell, item_value=1):
    # For notebook["nbformat"] >=4
    if "execution_count" in cell.keys():
        return cell["outputs"][item_value]['data']['image/png']
    # For notebook["nbformat"] < 4
    elif "prompt_number" in cell.keys(): # i.e version < 4
        return cell["outputs"][item_value]['png']
    # In case we missed anything, or changes in the future
    return None
```

This is a brief summary of all the steps from finding the correct cell to displaying the desired image:

```
from IPython.display import Image

out_value = 11 # example value
item_value = 1 # example value
cell = select_cell(notebook, out_value)
Image(cell_to_image(cell, item_value))
```
* `out_value` and `item_value ` are as described above

### Putting it all together: reading from numerous notebooks

Summarising the above, here we bundle the results into a loop.  
 
This script displays images  from the same exact output line (`out_value=6`) of `.ipynb` notebooks as listed in a given `list_file_notebook`:  
```
from IPython.display import Image, display
import nbformat

notebook_version = 4
outvalue = 6
out_item_val = 0

for ifile, file_temp in enumerate(list_file_notebook):
    # Reading in Notebook
    notebook_temp = nbformat.read(file_temp, notebook_version)
    
    # Finding Cell of `out_value`
    cell_temp = select_cell(notebook_temp, outvalue)
    
    # Extracting string information from the cell
    str_image = cell_to_image(cell_temp, item_value = out_item_val)
    
    # Displaying the image
    display(Image(str_image))
```

**Results and Summary**

In our [toy demo](https://github.com/cambridgeanalytica/jupyterstream/tree/master/demo) we examine the distribution of registration dates by state. 

The actions we take:
* We create a notebook [`my_notebook.ipynb`](https://github.com/cambridgeanalytica/jupyterstream/blob/master/demo/notebooks/my_notebook.ipynb) that, given the variable `state_abrv`, displays the information of the state. 
* We call `runipy_wrapper` which clones  `my_notebook.ipynb` into  `my_notebook_[state_abrv].ipynb` and then runs this clone with `runipy`.  
In which, `runipy_wrapper` passes to the clone notebook the argument by `os.["state_abrv"] = state_abrv`. In the clone we call the argument by `state_abrv = os.environ["state_abrv"]`.
* In the Appendix below, we show how to run `runipy_wrapper` for multiple `state_abrv` values in parallel using `parallel`.
* We then use a master notebook [`my_noteook_master.ipynb`](https://github.com/cambridgeanalytica/jupyterstream/blob/master/demo/notebooks/my_notebook_master.ipynb) that reads and displays information from all of the clones.

In the following figure we show the results for a handful of states, segmented by party affilation.

As for the resulting figure, as expected, because the General Elections in 2008 and 2012 were held in November we clearly see prior to that an increase in the registration rate.

<img src="blog-runipy/jupyterstream_image_02c.png" width="1000">



### Appendix: Parallelising with `parallel`
As our database is partitioned by the 51 states, and some of which are quite large (e.g, California, Florida and Texas) we would like to run our jobs in parallel. 

We use the shell command line function `parallel`. A common call would be: 
```
parallel -j 4 python runipy_wrapper.py -state_abrv {1} ::: AK AR AZ CO CT DC DE FL
```
This reads- 
>Run on four servers in parallel the command: `python runipy_wrapper.py -state_abrv [state_abrv]`


This is a handy script to create (and generalize) this command: 

```
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
```

To demonstrate the use of this function we have prepared a [demo](https://github.com/cambridgeanalytica/jupyterstream/tree/master/demo).
