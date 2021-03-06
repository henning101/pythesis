import os
import json
from flask import Flask, request, send_from_directory, request
from flask import render_template
from flask_cors import CORS
import pythesis.argparser as argparser
from pythesis.transpiler import Transpiler
from pythesis.compiler import Compiler

app = Flask(
    __name__, 
    static_url_path='/',
    template_folder=os.path.abspath('./app/build'),
    static_folder=os.path.abspath('./app/build')
)
CORS(app)

@app.route('/')
def send_js():
    return send_from_directory(os.path.abspath('./app/build'), 'index.html')

@app.route('/args')
def args():
    return app.response_class(
        response=json.dumps(vars(argparser.args), indent=2),
        status=200,
        mimetype='application/json'
    )

@app.route('/pdf')
def pdf():
    args = argparser.args
    return send_from_directory(
        os.path.abspath(f'{args.project_root}/build'), 
        f'{args.main_document}.pdf'
    )

@app.route('/full_build')
def full_build():
    args = argparser.args
    transpiler = Transpiler()
    transpiler.transpile(full=True)
    compiler = Compiler()
    compiler.compile()
    return 'Done'

@app.route('/partial_build')
def partial_build():
    args = argparser.args
    transpiler = Transpiler()
    transpiler.transpile(full=False)
    compiler = Compiler()
    compiler.compile()
    return 'Done'

@app.route('/partial_execute')
def partial_execute():
    transpiler = Transpiler()
    transpiler.transpile(full=False)
    return 'Done'
