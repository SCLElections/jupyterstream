#jupyterstream
**Data delivery streamlines simplified by handy manipulations of Jupyter notebooks**  
This code accompanies [our blog](http://wiki.cambridgeanalytica.net/blog-runipy) which discusses the benefits of usage of `runipy`, parallelising executions and aggreating the results in one master notebook using `nbformat`.

In detail we discuss:  
* Applying [`runipy`](https://pypi.python.org/pypi/runipy), a convienient tool to run a notebook from the command line
* Parallelising executions the bash command `parallel`.   
* Using [`nbformat`](https://nbformat.readthedocs.io/en/latest/format_description.html), a python module to read text and image outputs from notebooks.  

We suggest using `runipy` to loop over notebooks or to run in parallel. Once the notebooks runs are completed, to figure out which runs were succesful and which require special attention,  a master notebook could collect the important metrics and figures (!) for analysis. 


***Disclaimer:*** *This is not an exhaustive explanation of the functionality of `runipy`, `nbformat` or `parallel`, but rather a suggestion from which one can develop their own preference of use.* 

# Demo

## Setup
To run the demo you will need to modify within `demo_path.py` the path to this `jupyterstream` location.  


## `runipy_wrapper.py`

After completing the [setup](https://github.com/cambridgeanalytica/public/tree/master/jupyterstream#setup), to examine (but not run) the `runipy` command for one state (e.g, Washington DC): 
```
python runipy_wrapper.py -state_abrv DC
```

To execute on one state (e.g, Washington DC) add the `-run` flag is in:  
```
python runipy_wrapper.py -state_abrv DC -run
```

## `parallel_run.py`

To examine (but not run) the `parallel` command on all states on 4 servers: 
```
python parallel_run.py -parallel 4
```

To execute parallel runs on 4 servers add the `-run` flag is in:
```
python parallel_run.py -parallel 4 -run
```
