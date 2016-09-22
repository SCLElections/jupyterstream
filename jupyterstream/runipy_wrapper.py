import numpy as np
import os
import sys


from os import environ
from subprocess import call

"""
str_var -  string of argument to pass
val     - the value to be passed
run - boolean safty. True: to execute, False: No execution but will dispaly the runipy command to run.

notebook_runs - auxiliary path suggested to store new notebooks
"""

#=========== Update Details ============
# --- path details
# directory of original notebook
notebook_dir = "/home/eyalk/projects/blog/runipy/notebooks/" # directory of original notebook  
# directory of the cloned notebooks
notebook_dirnew = notebook_dir + "notebook_runs/" # directory of new notebook  
# name of the original notebook (without extension .ipynb)
notebook_prefix = "my_notebook" 

# --- variable details
str_var = "state_abrv"
#=======================================

# safty
run = False

# keyword to perform multi-runs over
val = None                                                                                                                   

# Calling system arguments
for iarg, arg in enumerate(sys.argv[1:]):
    if "-run" == arg: run = True
    if "-{}".format(str_var) == arg: val = sys.argv[iarg + 2]

notebook = "{}{}.ipynb".format(notebook_dir,notebook_prefix)
notebook_new = "{}{}_{}.ipynb".format(notebook_dirnew, notebook_prefix, val)

# creating the new notebook
if run:
    print "Creating {}".format(notebook_new)
    os.system("cp %s %s"%(notebook,notebook_new)) 

# creating the bash line command (for display)
str_command = "{}={} runipy -o {}".format(str_var, val, notebook_new)
print "=================================================="
print str_command
print "=================================================="

# execution
if run:
    environ[str_var] = val
    call(["runipy","-o", notebook_new])
else:
    print "(The above is the ruinpy call, but it did not run.) To execute, add the flag: -run "