#DEMO: `jupyterstream`
**Data delivery streamlines simplified by handy manipulations of Jupyter notebooks**  
This code accompanies [our blog](http://wiki.cambridgeanalytica.net/blog-runipy) which discusses the benefits of usage of `runipy`, parallelising executions and aggreating the results in one master notebook using `nbformat`.

![Alt text](../png/jupyterstream.png?raw=true "Title")

***Disclaimer:*** *This is not an exhaustive explanation of the functionality of `runipy`, `nbformat` or `parallel`, but rather a suggestion from which one can develop their own preference of use.* 

## Setup
For the demo to work you need to change 'path' in 'demo_path.py' to this directory ('[...]/jupyterstream/demo/')  
To run the parallelisation part, the GNU [`parallel`](http://savannah.gnu.org/projects/parallel/) is required.

## `runipy_wrapper.py`

After completing the [setup](https://github.com/cambridgeanalytica/public/tree/master/jupyterstream#setup), to examine (but not run) the `runipy` command for one state (e.g, Washington DC): 
```
python demo_runipy.py -l DC
```

To execute on one state (e.g, Washington DC) add the `--run` flag is in:  
```
python demo_runipy.py -l DC --run
```
This will create a subfolder in `[...]/jupyterstream/demo/notebooks/` called `notebook_runs`. Within should be an executed notebook called `my_notebook_DC.ipynb`.  

## `parallel_run.py`
To run the parallelisation part, the GNU [`parallel`](http://savannah.gnu.org/projects/parallel/) is required.  

To examine (but not run) the `parallel` command on a few variables on 3 servers: 
```
python demo_runipy.py -j 3 -l AK,AR,AZ,CO,CT,DC
```

To execute parallel runs on 3 servers add the --run flag is in:
```
python demo_runipy.py -j 3 -l AK,AR,AZ,CO,CT,DC --run
```
Within  `notebook_runs` should be 31 executed notebooks ([only 32 states](http://www.huffingtonpost.com/2014/05/27/state-party-registration_n_5399977.html) require party registration; Here we exclude California).

To run all the 31 states  
```
python demo_runipy.py -j 4 -l AK,AR,AZ,CO,CT,DC,DE,FL,IA,ID,KS,KY,LA,MA,ME,MD,NC,NE,NH,NJ,NM,NV,NY,OK,OR,PA,RI,SD,UT,WV,WY --run
```

## Master Notebook
We also demo a "master" notebook that collects the important metrics and figures for analysis.  
See `[...]/jupyterstream/notebooks/my_notebook_master.ipynb` for details. 
