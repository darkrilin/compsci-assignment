from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import main
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mat'}
HEROKU = os.environ.get('HEROKU', 0)

if HEROKU == 0:
    print("Offline")
    UPLOAD_FOLDER = "/uploads/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.isdir(d):
        os.makedirs(d)


@app.route('/')
def show_main():
    return render_template('website.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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

        for each_file in uploaded_files:

            if each_file and allowed_file(each_file.filename):
                filename = secure_filename(each_file.filename)

                try:
                    ensure_dir(app.config['UPLOAD_FOLDER'])
                    each_file.save(app.config['UPLOAD_FOLDER'] + filename)
                    files_to_process.append(filename)
                except PermissionError:
                    return redirect('/static/upload_error.html')

        # now do the processing
        if len(files_to_process) == 0:
            # redirect if none of the files are uploaded correctly
            return redirect('/static/upload_error.html')

        elif len(files_to_process) == 1:
            # only one file selected, graph normally
            current_file = files_to_process[0]
            try:
                main.bokeh_composite(app.config['UPLOAD_FOLDER'] + current_file, auto_open=False)
                session['composite_path'] = '/graph/' + current_file[:-4] + '_composite' + '.html'
                return redirect('/graph/' + current_file[:-4] + '_composite' + '.html')
            except KeyError:
                return redirect('/static/key_error.html')

        elif len(files_to_process) > 1:
            # graph all files into same document
            print(files_to_process)

            # TODO: CREATE FUNCTION IN main.py WHICH HANDLES MULTIPLE GRAPH FILES

        # fail safe
        return redirect("/")


@app.route('/composite')
def composite_selected():
    return redirect(session['composite_path'])


@app.route('/graph/<filename>')
def graph_file(filename):
    try:
        file = open(app.config['UPLOAD_FOLDER'] + filename)
    except Exception as ex:
        print(ex)
        return redirect('/')

    file_html = file.read()
    file.close()
    return file_html


@app.route('/example')
def example():
    return redirect("/static/example.html")


def insert_substring(main_string, substring, index):
    return main_string[:index] + substring + main_string[index:]


app.secret_key = os.environ.get('SECRET_KEY', None)
if app.secret_key is None:
    print("Secret key not found. Exiting app.")
    exit()
else:
    if HEROKU:
        PORT = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=PORT)
    else:
        app.run(host='localhost')
