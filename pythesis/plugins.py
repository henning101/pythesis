class Execute(Extension):
    """ Allows to execute Python files.
    """
    tags = set(['exec'])

    def __init__(self, environment):
        super(Execute, self).__init__(environment)
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
