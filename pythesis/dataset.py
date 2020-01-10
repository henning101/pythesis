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

    def nan_to_num(self):
        """ Converts NaN values to 0 and infinite values to large numbers.
        """
        self.data = np.nan_to_num(self.data, nan=0)

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

        # Create a new column dictionary using aliases:
        aliased = {}
        for key, column in self.columns.items():
            if 'alias' in column.attr:
                aliased[column.attr['alias']] = column
            else:
                aliased[key] = column 
        self.columns = aliased

    def extend(self, dataset):
        """ This method extends this dataset with another dataset. All column
        keys in this dataset must be present in the input dataset.
        """
        d = dataset.to_dict()
        for key, column in self.columns.items():
            # Extend the column using the respective column from the input 
            # dataset:
            column.data.extend(d[key])

    def to_dict(self):
        """ Returns the dataset as a dictionary.
        """
        d = {}
        for key, column in self.columns.items():
            d[key] = column.data
        return d

    def crop(self, start, end):
        """ Crops the dataset in-place using a start and end value.
        """
        for key, column in self.columns.items():
            column.data = column.data[start:end]

    def crop_by_column(self, key, min, max):
        """ Crops the dataset in-place before the min and after the max value of
        the respective column. 
        """
        column = self.columns[key]
        start = None
        end = None
        # Find the crop indices:
        for i in range(len(column.data)):
            value = column.data[i]
            if value >= min and start == None:
                start = i 
            if value >= max and end == None:
                end = i

        # Default case:
        if start == None:
            start = 0
        if end == None:
            end = len(self.columns[key].data) - 1
        self.crop(start, end + 1)

    def nan_to_num(self):
        """ Executes nan_to_num for all columns of the dataset.
        """
        for key, column in self.columns.items():
            column.nan_to_num()

def combine(datasets):
    """ Combines a list of datasets by extending the first dataset with all
    remaining sets and the returning the first.
    """
    first = datasets[0]
    for i in range(1, len(datasets)):
        first.extend(datasets[i])
    return first

def load_dataset(csv_file, columns=[]):
    dataset = Dataset()
    dataset.from_csv(csv_file, columns)
    return dataset
