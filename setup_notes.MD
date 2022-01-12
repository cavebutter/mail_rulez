# Setup Notes

## Major Changes

### Move 'standalone' modules to standalone directory
These are modules that just exist to call specialized functions such as processing the _vendor folder.  They were crowding up the main directory.

### setup.py
This script will take user input to create or modify the config file.

Will also launch the appropriate maint program.