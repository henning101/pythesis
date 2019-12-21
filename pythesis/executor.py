import os
import sys
import logging
import matplotlib
import matplotlib.pyplot as _plt
import numpy as _np
import json
import importlib
from io import StringIO
import pythesis.argparser as argparser
import pythesis.dataset as _dataset
from pythesis.dataset import Dataset
from pythesis.template import Template, Templater

# Singletons that can be used from within LaTeX:
_matlab     = None
_templater  = None

# Variables:
_project    = None
_data       = None
_build      = None
_lib        = None
_templates  = None
_file       = None 
_dir        = None 
_basename   = None 
_name       = None 

def init():
    """ Initializes the singletons that can be used within LaTeX. Note that the
    transpiler currently only supports a single-thread execution. Multi-thread
    execution would require a different architecture (e.g. a mediator).
    """
    global _matlab 
    global _templater
    global _logger
    global _project 
    global _data 
    global _build
    global _lib
    global _templates
    # Initialize the MATLAB adapter:
    if argparser.args.matlab:
        from pythesis.matlab_adapter import MatlabAdapter
        _matlab = MatlabAdapter()
        _matlab.connect()

    _project    = argparser.args.project_root
    _data       = f'{_project}/data'
    _build      = f'{_project}/build'
    _templates  = f'{_project}/templates'
    _lib        = f'{_project}/lib'
    _templater  = Templater()

def _wrap(module):
    importlib.reload(module) # Make sure the module is updated
    module._matlab      = _matlab
    module._templater   = _templater
    module._project     = _project 
    module._dataset     = _dataset
    module._data        = _data 
    module._build       = _build 
    module._lib         = _lib
    module._templates   = _templates
    module._file        = _file
    module._dir         = _dir 
    module._basename    = _basename
    module._name        = _name
    module._np          = _np
    module._plt         = _plt

def execute(path):
    global _file
    global _dir
    global _basename
    global _name

    _file = path
    _dir = os.path.dirname(path)
    _basename = os.path.basename(_file)
    _name = os.path.splitext(_basename)[0]
  
    # Store the current working directory: 
    cwd = os.getcwd()
    # Change into the file directory:
    os.chdir(_dir)
    # Temporarily add current directory to sys path:
    sys.path.append(_dir)
    original = sys.stdout
    capture = sys.stdout = StringIO()
    with open(path) as f:
        exec(f.read())
    sys.stdout = original
    result = capture.getvalue()
    capture.close()
    # Remove current directory from system path:
    sys.path.remove(_dir)
    # Change back into the previous working directory:
    os.chdir(cwd)
    # Log result:
    logging.getLogger(__name__).info(result)
    return result
