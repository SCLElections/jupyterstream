#jupyterstream
**Data delivery streamlines simplified by handy manipulations of Jupyter notebooks**  
This code accompanies [our blog](http://wiki.cambridgeanalytica.net/blog-runipy) which discusses the benefits of usage of `runipy`, parallelising executions and aggreating the results in one master notebook using `nbformat`.

![Alt text](./png/jupyterstream.png?raw=true "Title")

In detail we discuss:  
* Applying [`runipy`](https://pypi.python.org/pypi/runipy), a convienient tool to run a notebook from the command line
* Parallelising executions the bash command `parallel`.   
* Using [`nbformat`](https://nbformat.readthedocs.io/en/latest/format_description.html), a python module to read text and image outputs from notebooks.  

We suggest using `runipy` to loop over notebooks or to run in parallel. Once the notebooks runs are completed, to figure out which runs were succesful and which require special attention,  a master notebook could collect the important metrics and figures (!) for analysis. 


***Disclaimer:*** *This is not an exhaustive explanation of the functionality of `runipy`, `nbformat` or `parallel`, but rather a suggestion from which one can develop their own preference of use.* 




# Setup
```
python setup.py install 
```
or 
```
python setup.py develop
```


# Demo

## Setup
To run the demo you will need to modify within `demo_path.py` the path to this `jupyterstream` location.  
To run the parallelisation part, the GNU [`parallel`](http://savannah.gnu.org/projects/parallel/) is required.

## `runipy_wrapper.py`

After completing the [setup](https://github.com/cambridgeanalytica/public/tree/master/jupyterstream#setup), to examine (but not run) the `runipy` command for one state (e.g, Washington DC): 
```
python runipy_wrapper.py -state_abrv DC
```

To execute on one state (e.g, Washington DC) add the `-run` flag is in:  
```
python runipy_wrapper.py -state_abrv DC -run
```
This will create a subfolder in `[...]/jupyterstream/notebooks/` called `notebook_runs`. Within should be an executed notebook called `my_notebook_DC.ipynb`.  

## `parallel_run.py`

To examine (but not run) the `parallel` command on all states on 4 servers: 
```
python parallel_run.py -parallel 4
```

To execute parallel runs on 4 servers add the `-run` flag is in:
```
python parallel_run.py -parallel 4 -run
```
Within  `notebook_runs` should be 31 executed notebooks ([only 32 states](http://www.huffingtonpost.com/2014/05/27/state-party-registration_n_5399977.html) require party registration; Here we exclude California).

## Master Notebook
We also demo a "master" notebook that collects the important metrics and figures for analysis.  
See `[...]/jupyterstream/notebooks/my_notebook_master.ipynb` for details. 
