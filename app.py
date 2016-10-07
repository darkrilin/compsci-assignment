from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import main
import os

UPLOAD_FOLDER = 'uploads/'
STATIC_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['mat'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.static_folder = os.getcwd()+STATIC_FOLDER

# I just want to say Will, I am so very sorry for anything
# I may have done to your precious files. Hopefully you can still
# test this thing locally, because it sort of works on heroku now.

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
            main.plotly_scatter(app.config['UPLOAD_FOLDER'] + filename, auto_open=False)
            os.remove(app.config['UPLOAD_FOLDER'] + filename)
            return redirect('/graph/' + filename + '.html')
        return redirect("/")

@app.route('/graph/<filename>')
def graph_file(filename):
    try:
        file = open(app.config['UPLOAD_FOLDER'] + filename)
    except:
        return redirect('/')
    file_html = file.read()
    file.close()
    #os.remove(app.config['UPLOAD_FOLDER'] + filename)
    return file_html


PORT = int(os.environ.get('PORT', 5000))
HEROKU = os.environ.get('HEROKU', 0)
if HEROKU:
    app.run(host='0.0.0.0', port=PORT)
else:
    app.run(host='localhost')