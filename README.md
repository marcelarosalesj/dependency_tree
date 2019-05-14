# dependency_tree

## Information
This project uses python3.


## Usage
```
# Generate buildtime and runtime xml and dot files 
python stx_dependency_tree.py -g buildtime
python stx_dependency_tree.py -g runtime

# Generate a graph and search on it
python stx_dependency_tree.py -g buildtime -s controllerconfig

# Search using an input xml
python stx_dependency_tree.py -i results/buildtime.xml -s controllerconfig
```
