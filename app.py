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

        #file = request.files['file']
        uploaded_files = request.files.getlist("file")
        print(uploaded_files)


        if (len(uploaded_files)) == 0:
            print("Redirecting to request URL")
            return redirect(request.url)


        for file in uploaded_files:
            print(file.filename)

            # TODO: LOOP THROUGH FILES, SAVE EACH INDIVIDUAL ONE
            # TODO: THEN PASS THROUGH A LIST OF FILES TO BE PROCESSED BY PYTHON

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                try:
                    ensure_dir(app.config['UPLOAD_FOLDER'])
                    file.save(app.config['UPLOAD_FOLDER'] + filename)

                except PermissionError:
                    return redirect('/static/uploaderror.html')

                try:
                    main.bokeh_composite(app.config['UPLOAD_FOLDER'] + filename, auto_open=False)

                    session['menu_active'] = False  # Disable 'BACK' button
                    session['composite_path'] = '/graph/' + filename[:-4] + '_composite' + '.html'
                    return redirect('/graph/' + filename[:-4] + '_composite' + '.html')

                except KeyError:
                    return redirect('/static/keyerror.html')

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
    if session['menu_active']:
        start_index = file_html.find('<body>') + len('<body>')
        sub = '<button id="back" style="z-index:1000;position:absolute;background-color: #447bdc;color: white; \
                padding: 14px;font-size: 16px;border: none;cursor: pointer;min-width: 300px;min-height: 50px; \
                margin-left:auto;margin-right:auto;border-radius: 5px;text-transform: uppercase;">Back</button> \
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>'
        file_html = insert_substring(file_html, sub, start_index)

        start_index = file_html.find('<script type="text/javascript">') + len('<script type="text/javascript">')
        sub = '$(document).ready(function(){$("#back").click(function(){window.location.replace("/select");});});'
        file_html = insert_substring(file_html, sub, start_index)
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
