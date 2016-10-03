from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import parsematlab_rats
import mainstuff
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['mat'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def ensure_dir(f):
    d = os.path.dirname(os.getcwd() + f)
    if not os.path.exists(d):
        os.makedirs(d)

@app.route('/')
def show_main():
    return render_template('website.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
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
            mainstuff.plot_with_plotly(app.config['UPLOAD_FOLDER'] + filename)
            os.remove(app.config['UPLOAD_FOLDER'] + filename)
            return redirect('/graph/' + filename + '.html')
        return redirect("/")


@app.route('/graph/<filename>')
def graph_file(filename):
    file = open(app.config['UPLOAD_FOLDER'] + filename)
    file_html = file.read()
    file.close()
    os.remove(app.config['UPLOAD_FOLDER'] + filename)
    return file_html
