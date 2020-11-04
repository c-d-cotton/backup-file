#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

def backupfile(backuploc, filename):
    """
    Backup file by full filename and backuploc.
    """
    import datetime
    import shutil

    thedir = os.path.dirname(backuploc + filename)
    if not os.path.isdir(thedir):
        os.makedirs(thedir)
    shutil.copyfile(filename, backuploc + filename + datetime.datetime.now().strftime('%y.%m.%d.%H.%M'))


def backuplist(backuploc, bulist):

    if backuploc[-1] == '/':
        backuploc = backuploc[:-1]

    bulist = [os.path.abspath(filename) for filename in bulist]
    while len(bulist) > 0:
        item = bulist.pop()

        if os.path.islink(item):
            print(item + ' is link so skipped.')
            continue
        if os.path.isfile(item):
            backupfile(backuploc, item)
        if os.path.isdir(item):
            if item[-1] != '/':
                item = item + '/'
            bulist.append([item + filename for filename in os.listdir(item)])
