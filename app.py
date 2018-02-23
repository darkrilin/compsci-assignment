from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import main

from os.path import dirname as os_dir_name, isdir as os_isdir, join as os_path_join
from os import environ as os_environ, makedirs as os_make_dirs, remove as os_remove

UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = {'mat'}
HEROKU = os_environ.get('HEROKU', 0)

app = Flask(__name__, static_url_path="")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def ensure_dir(f):
    d = os_dir_name(f)
    if not os_isdir(d):
        os_make_dirs(d)


@app.route('/')
def show_main():
    return render_template('website.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        session['output_path'] = ""

        # check if the post request has the file part
        if 'file' not in request.files:
            print("Redirecting to request URL")
            return redirect(request.url)

        # get list of files sent through from jquery
        uploaded_files = request.files.getlist("file")

        if (len(uploaded_files)) == 0:
            print("Redirecting to request URL")
            return redirect(request.url)

        # loop through and save all uploaded files
        files_to_process = []
        upload_path = os_path_join(app.root_path + app.config['UPLOAD_FOLDER'])
        static_path = os_path_join(app.root_path + '/static/graphs/')
        ensure_dir(upload_path)
        ensure_dir(static_path)

        for each_file in uploaded_files:
            if each_file and allowed_file(each_file.filename):
                filename = secure_filename(each_file.filename)
                try:
                    each_file.save(upload_path + filename)
                    files_to_process.append(upload_path + filename)
                except PermissionError:
                    return redirect('/upload_error.html')

        # now do the processing
        if len(files_to_process) == 0:
            # redirect if none of the files are uploaded correctly
            return redirect('/upload_error.html')

        elif len(files_to_process) == 1:
            # only one file selected, graph normally
            current_file = files_to_process[0]
            try:
                main.graph_single(current_file, auto_open=False, dir=static_path)
                session['output_path'] = os_path_join('/graphs/' + current_file.split("/")[-1][:-4] + '.html')
            except KeyError:
                return redirect('/key_error.html')

        elif len(files_to_process) > 1:
            # graph all files into same document
            main.graph_multiple(files_to_process, scatter=True, heatmap=True, auto_open=False)
            print(files_to_process)
            # TODO: CREATE FUNCTION IN main.py WHICH HANDLES MULTIPLE GRAPH FILES

        # clean up temp files
        for file in files_to_process:
            os_remove(file)

        # redirect to output graph
        return redirect('/output')


@app.route('/output')
def output_graph():
    return redirect(session['output_path'])


@app.route('/example')
def example():
    return redirect("example.html")


def insert_substring(main_string, substring, index):
    return main_string[:index] + substring + main_string[index:]


app.secret_key = os_environ.get('SECRET_KEY', None)
if app.secret_key is None:
    print("Secret key not found. Exiting app.")
    exit()
else:
    if HEROKU:
        PORT = int(os_environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=PORT)
    else:
        app.run(host='localhost')
