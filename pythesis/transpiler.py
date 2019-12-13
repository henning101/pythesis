import os
import sys
import codecs
import jinja2
import shutil
import logging
import json
import re
from jinja2 import Template
from jinja2.ext import Extension
import pythesis.argparser as argparser
import pythesis.executor as executor

class SubInclude(Extension):
    """ Allows to import relative files.
    """
    tags = set(['subinclude'])
    
    def __init__(self, environment):
        super(SubInclude, self).__init__(environment)
        self.matcher = re.compile('\.*')

    def parse(self, parser):
        node = parser.parse_include()
        template = node.template.as_const()
        cur_path = parser.name.split('/')
        cur_path.pop() # Pop current file name from path
        abspath = '/'.join(cur_path) + '/' + template

        # Automatically append the .tex extension:
        if not(abspath.endswith('.tex')):
            abspath = abspath + '.tex'

        node.template.value = abspath
        return node

class Transpiler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.args = argparser.args 

    def transpile(self, full=False):
        """ Transpiles the document.
        """
        # Execute the Python scripts:
        self.execute(full)
        # Transpile the LaTeX document: 
        loader = jinja2.FileSystemLoader(searchpath=f'{self.args.project_root}/src')
        # Add the subinclude extension:
        env = jinja2.Environment(loader=loader, extensions=[SubInclude])
        template = env.get_template(f'{self.args.main_document}.tex')
        output_path = f'{self.args.project_root}/build/{self.args.main_document}.tex'
        # Render the template to the output .tex file: 
        with codecs.open(output_path, 'w', 'utf-8') as f:
            f.write(template.render())

    def execute(self, full=False):
        """ Recursively executes all Python files in the project_root
        """
        for root, directories, filenames in os.walk(f'{self.args.project_root}/src'):
            # Files in the _.always list are always executed (during a full
            # AND a partial build):
            always_list = self.always_list(root)
                
            for filename in filenames:
                if filename.endswith('.py'):
                    # Ignore files that start with an underscore:
                    if not(filename.startswith('_')):
                        # Execute if a full build is running or the file is in the
                        # _.always list:
                        if full or filename in always_list:
                            self.execute_file(root, filename)

    def execute_file(self, root, filename) :
        """ Loads a .py file and passes it to the executor. 
        """
        path = os.path.join(root, filename)
        base = os.path.basename(path)
        name = os.path.splitext(base)[0]
        texfilename = f'{name}.tex'
        result = executor.execute(path)

        _texpath = os.path.join(root, '../_tex')
        if not(os.path.isdir(_texpath)):
            os.makedirs(_texpath)
        outpath = os.path.join(_texpath, texfilename)
        with open(outpath, 'w+') as outfile:
            outfile.write(result)

    def always_list(self, root):
        """ Creates a file list from the _.always file in a directory if it
        exists.
        """
        result = []
        filenames = [] 
        always_path = os.path.join(root, '_.always')
        if os.path.isfile(always_path):
            with open(always_path) as f:
                filenames = f.read().splitlines()
        for name in filenames:
            if not(name.endswith('.py')):
                result.append(f'{name}.py') # Append .py extension
            else:
                result.append(name)
        return result
