import os
import re
import json
import jinja2
from jinja2 import Template
from jinja2.ext import Extension
import pythesis.argparser as argparser

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

class Templater: 
    def render(self, _path, **args):
        template = Template(_path)
        return template.render(**args)

class Template:
    """ Represents a template file that can be populated using an accompanying
    defaults JSON file and user variables. 
    """
    def __init__(self, _path):
        dirname = os.path.dirname(_path)
        basename = os.path.basename(_path)
        name = os.path.splitext(basename)[0]
        self.load_template(_path)

        # Try to find an accompanying defaults JSON file:
        self.defaults = {} # Start with an empty defaults dictionary
        defaults_path = f'{dirname}/{name}.json'
        if os.path.isfile(defaults_path):
            with open(defaults_path, 'r') as f:
                self.defaults = json.loads(f.read())

    def render(self, **args):
        """ Adds user args to the template defaults and returns the rendered
        template.
        """
        jinja_template = jinja2.Template(self.template)
        for key, value in args.items():
            self.defaults[key] = value
        return jinja_template.render(**self.defaults)

    def load_template(self, _path):
        with open(_path, 'r') as f:
            self.template = f.read()

def render(_path, args):
    template = Template(_path)
    return template.render(args)

if __name__ == '__main__':
    t = Template(os.path.abspath('../example/templates/matlab/pdf.m'))
