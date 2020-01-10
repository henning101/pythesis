import os
import json
import time
import traceback
import logging
import matlab.engine
import pythesis.utils
from pythesis.dataset import Dataset
from pythesis.template import Template, Templater

class MatlabAdapter:
    """ Adapter class that provides functions to interact with the Python
    MATLAB engine.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.eng = None

    def connect(self):
        """ Connects to the first shared MATLAB session.
        """
        if self.eng == None:
            try:
                engine_names = matlab.engine.find_matlab()
                if len(engine_names) == 0:
                    self.logger.error('No available MATLAB sessions')
                    self.logger.error('To share the MATLAB engine execute: matlab.engine.shareEngine')
                    time.sleep(1)
                    self.connect()
                else:
                    self.logger.info(f'Available MATLAB sessions: {engine_names}')
                    self.eng = matlab.engine.connect_matlab(engine_names[0])
                    self.logger.info(f'Connected to {engine_names[0]}')
            except Exception as e:
                self.logger.error(str(e))
                time.sleep(1)
                self.connect() # Retry 
        
    def load_dataset(self, path, name, columns, **attr):
        """ Loads a dataset into MATLAB.
        """
        # Create the dataset:
        dataset = Dataset(**attr)
        # Load from CSV file using selected columns:
        dataset.from_csv(path, columns)
        self.insert_dataset(name, dataset)

    def insert_dataset(self, name, dataset):
        # Generate dictionary:
        data = dataset.to_dict()
        # Create a new empty dictionary to pass to MATLAB:
        matlab_data = {}
        # Convert float columns to MATLAB double arrays:
        for key, column in dataset.columns.items():
            if column.attr['datatype'] == 'float':
                # We need to transpose the MATLAB double object in order to
                # create a column vector:
                matlab_double = self.eng.transpose(matlab.double(data[key]))
                matlab_data[key] = matlab_double
        # Pass data to MATLAB
        self.eng.workspace[name] = matlab_data 

    def insert_value(self, key, value):
        self.eng.workspace[key] = float(value)

    def matlab_double(self, data):
        return matlab.double(data)

    def eval(self, cmd, nargout=0):
        """ Forwards a MATLAB command to the engine with default number of
        arguments set to 0.
        """
        try:
            cmd = cmd.replace("'", "\'")
            self.eng.eval(cmd, nargout=nargout)
        except Exception:
            self.logger.error(f'Error in command: {cmd}')
            self.logger.error(traceback.format_exc())

    def eval_template(self, _path, **args):
        templater = Templater()
        cmd = templater.render(_path, **args)
        self.logger.info(cmd)
        self.eval(cmd)
