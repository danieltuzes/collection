# Voilà example

This is a Jupyter Voilà example how a minimalist web application looks like. You can hardly change the design but content can be easily modified or added. Voilà turns a Jupyter notebook into a web application with the help of Jupyter widgets which could potentially be used in onsite Jupyter notebooks too, but are not used, because modifying the source code is convenient and simple therefore one does not think about using widgets.

In my other flask example I have full control over the design, content and code, but it also means that I have to provide the glue between

- HTML request,
- python calculation and
- rendering the result
- return server response

Here I only have to have a python environment with the proper python packages, write the python code, and nothing else (wqeb query, webserver, HTML) needs to be taken care of.

## Usage

cd into the folder where the jupyter notebook can be found and [start voilà with](https://voila.readthedocs.io/en/stable/using.html#as-a-standalone-application)

```bash
voila compound_interest.ipynb --MappingKernelManager.cull_interval=3600 --MappingKernelManager.cull_idle_timeout=7200
```

The last two options tells the underlying jupyter server to check for idle kernels every hour and those which are idle for more than 7200 seconds, are terminated. This helps to protect the memory.
