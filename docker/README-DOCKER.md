
This approach is painful so not using it yet.

## Build Dockerfile
In the root of wandergrove, run 
```docker build -f Dockerfile.dev -t wandergrove_dev .```



## Starting Environment

Start by pulling the latest gds_env docker image:
```docker pull darribas/gds_dev:10.0```

Once that is pulled, run:
```docker run -d --name gds_env -p 8888:8888 -v ${PWD}:/workspace darribas/gds_dev:10.0```

Then, go to the Remote Explorer, and find the running container. Attach to the running container in a **New Window**. This will open a new window inside the container.

### Running Python
You can run python scripts the normal way by running in the Terminal: 
```python {script_name}.py```

### Running Jupyter Notebook (via Jupyter)
You can run Jupyter Notebook by running in a terminal:
```jupyter notebook```

Copy the entire URL it gives you into your browser. Now you should be in Jupyter!

### Running Jupyter Notebook (via VS Code)
First, install the Jupyter & Python extensions in the remote container. You can do this normally, as you do in regular VS Code.

Then, open up your notebook, select the right Kernel, and you should be good to go! 