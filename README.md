# jupyterstream
**Python procedures streamlined by handy manipulations of Jupyter notebooks**  
This code accompanies [our blog](https://cambridgeanalytica.org/news/blog/1205) which discusses the benefits of usage of `runipy`, parallelising executions and aggreating the results in one master notebook using `nbformat`.

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
See the [`demo` folder](./demo/) for an example demonstration.  
