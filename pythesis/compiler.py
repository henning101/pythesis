import os
import logging
from jinja2 import Template
import pythesis.argparser as argparser

class Compiler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.args = argparser.args

    def compile(self):
        build_config = self.load_build_config()
        # Change into build directory:
        os.chdir(os.path.join(self.args.project_root, 'build'))
        # Execute build commands:
        for cmd in build_config:
            os.system(cmd)
        # Change back into pythesis directory:
        os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

    def load_build_config(self):
        #with open('./build.config') as f:
        with open(self.args.build_config) as f:
            template = Template(f.read())
            template = template.render(main_document=self.args.main_document)
        return template.splitlines()
