# General Modules
import sys
import os

# JupyterStream Modules
from jupyterstream import JupyterStream

"""
Demo Instructions

-- One Variable --

To examine (but not run) the runipy command for one state (e.g, Washington DC):
> python demo_runipy.py -l DC

To execute on one state (e.g, Washington DC) add the --run flag is in:
> python demo_runipy.py -l DC --run

-- Parallel Run of Mulitple Variables ---
Setup: To run the parallelisation part, the GNU parallel is required.

To examine (but not run) the parallel command on a few variables on 3 servers:
> python demo_runipy.py -j 3 -l AK,AR,AZ,CO,CT,DC                      

To execute parallel runs on 3 servers add the --run flag is in:
> python demo_runipy.py -j 3 -l AK,AR,AZ,CO,CT,DC --run

(For all states):
> python demo_runipy.py -j 12 -l AK,AR,AZ,CO,CT,DC,DE,FL,IA,ID,KS,KY,LA,MA,ME,MD,NC,NE,NH,NJ,NM,NV,NY,OK,OR,PA,RI,SD,UT,WV,WY --run

"""

#=========== Details - Demo Specific ============

# --- Demo notebook path details

import demo_path

# directory of original notebook
notebook_dir = "{}notebooks/".format(demo_path.path)
# name of the original notebook (without extension .ipynb)
notebook_prefix = "my_notebook"

notebook = "{}{}.ipynb".format(notebook_dir, notebook_prefix)
# directory of the cloned notebooks
notebook_dirnew = "{}notebook_runs/".format(notebook_dir) # directory of new notebook  

# --- Notebook Variable
str_val = "state_abrv"

# ---- calling this program during parallisation
bash_program = "python demo_runipy.py "
#===============

# ============ Argument passing preparation ==========
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-l","--list", help="list of variable comma separated (e.g: -l AK,AR,AZ)")
parser.add_argument("-r","--run", help="to execute", action="store_true")
parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-j","--jobs", help="run n jobs in parallel")
args = parser.parse_args()

list_vals =  args.list.split(",")
# =================================================

just = JupyterStream(run=args.run, verbose=args.verbose)

if len(list_vals) == 1:
    just.runipy_wrapper(list_vals[0], val_name=str_val, notebook_origin= notebook, notebook_prefix= notebook_prefix, notebook_dirnew=notebook_dirnew)
else:
    just.parallel_execute(bash_program, list_vals, jobs=args.jobs)