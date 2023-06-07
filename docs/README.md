## !!WARNING!!
### A few changes need to be made to generate the documentation correctly:
    1. adding an empty __init__.py file to the src folder - despite the fact that it is not a folder with a module, this step currently needs to be performed for correct documentation generation
    2. for some reason (wip, temporary solution), all *.py files need to comment out the imports related to the modules that are included in the project (for example, within the main.py file lines 2-4, within the workWithTransaction module line 2 etc. )