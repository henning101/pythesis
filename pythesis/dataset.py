import os
import csv
import json
import logging
import math
import numpy as np
from collections import OrderedDict

class Column:
    """ This class represents a single column in a dataset.
    """
    def __init__(self, attr={}):
        # Default attributes:
        self.attr = {
            'datatype': 'float',
            'offset': 0
        }
       
        # Overwrite default attributes: 
        for key, value in attr.items():
            self.attr[key] = value

        self.logger = logging.getLogger(__name__)
        self.data = []
    
    def append(self, item):
        """ Append a single datapoint to the columns.
        """
        if self.attr['datatype'] == 'float':
            # Datatype is float:
            try:
                # Add an offset to each datapoint:
                self.data.append(float(item) + self.attr['offset'])
            except ValueError:
                # Use 0 as default value, still add the offset:
                self.data.append(0 + self.attr['offset'])
        else:
            # Datatype is anything else:
            self.data.append(item)

class Dataset:
    """ Represents a dataset with one or more columns.
    """
    def __init__(self, **attr):
        self.columns = OrderedDict()
        # Set default attributes:
        self.attr = {
            'start': 1,
            'end': math.inf
        }

        # Update default attributes:
        for key, value in attr.items():
            self.attr[key] = value
        
    def from_csv(self, csv_file, columns=[]):
        """ Loads a dataset from a CSV file
        """
        self.columns = OrderedDict()
        for column in columns:
            self.columns[column['key']] = Column(column)
        i = 0
        header = []
        with open(csv_file) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if i == 0:
                    header = row # Store header
                else:
                    if i >= self.attr['start'] and i <= self.attr['end']:
                        j = 0
                        for header_key in header:
                            # Add item if header is selected:
                            if header_key in self.columns:
                                self.columns[header_key].append(row[j])
                            j = j + 1
                i = i + 1

    def to_dict(self):
        """ Returns the dataset as a dictionary.
        """
        d = {}
        for key, column in self.columns.items():
            d[key] = column.data
        return d 

def load_dataset(csv_file, columns=[]):
    dataset = Dataset()
    dataset.from_csv(csv_file, columns)
    return dataset
