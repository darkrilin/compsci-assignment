from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import main
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mat'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


@app.route('/')
def show_main():
    return render_template('website.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    scatter = True if request.form['scatter'] == 'true' else False
    heatmap = True if request.form['heatmap'] == 'true' else False
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ensure_dir(app.config['UPLOAD_FOLDER'])
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            try:
                if heatmap:
                    main.plotly_heatmap(app.config['UPLOAD_FOLDER'] + filename, radius=80, auto_open=False)
                if scatter:
                    main.plotly_scatter(app.config['UPLOAD_FOLDER'] + filename, auto_open=False)
                os.remove(app.config['UPLOAD_FOLDER'] + filename)
                if heatmap and scatter:
                    session['heatmap_path'] = '/graph/' + filename[:-4] + '_heatmap' + '.html'
                    session['scatter_path'] = '/graph/' + filename[:-4] + '_scatter' + '.html'
                    session['menu_active'] = True
                    return redirect('/select')
                elif heatmap:
                    session['menu_active'] = False
                    session['heatmap_path'] = '/graph/' + filename[:-4] + '_heatmap' + '.html'
                    if 'scatter_path' in session:
                        session.pop('scatter_path', None)
                    return redirect('/graph/' + filename[:-4] + '_heatmap' + '.html')
                elif scatter:
                    session['menu_active'] = False
                    session['scatter_path'] = '/graph/' + filename[:-4] + '_scatter' + '.html'
                    if 'heatmap_path' in session:
                        session.pop('heatmap_path', None)
                    return redirect('/graph/' + filename[:-4] + '_scatter' + '.html')
            except KeyError:
                return redirect('/static/keyerror.html')

        return redirect("/")


@app.route('/select/')
def select():
    return render_template('graph_selection.html')


@app.route('/scatter')
def scatter_selected():
    return redirect(session['scatter_path'])


@app.route('/heatmap')
def heatmap_selected():
    return redirect(session['heatmap_path'])


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
        sub = '<button id="back" style="z-index:1000;position:absolute;background-color: #447bdc;color: white;padding: 14px;font-size: 16px;border: none;cursor: pointer;min-width: 300px;min-height: 50px;margin-left:auto;margin-right:auto;border-radius: 5px;text-transform: uppercase;">Back</button><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>'
        file_html = insert_substring(file_html, sub, start_index)
        start_index = file_html.find('<script type="text/javascript">') + len('<script type="text/javascript">')
        sub = '$(document).ready(function(){$("#back").click(function(){window.location.replace("/select");});});'
        file_html = insert_substring(file_html, sub, start_index)
    return file_html


def insert_substring(main_string, substring, index):
    return main_string[:index] + substring + main_string[index:]


HEROKU = os.environ.get('HEROKU', 0)
app.secret_key = os.environ.get('SECRET_KEY', None)
if app.secret_key == None:
    print("Secret key not found. Exiting app.")
    exit
else:
    if HEROKU:
        PORT = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=PORT)
    else:
        app.run(host='localhost')
