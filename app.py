import os
from flask import Flask, render_template, url_for, send_from_directory, send_file, request
from decisiontree import *
from werkzeug.utils import secure_filename
import pandas as pd
import json

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.png', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    """Index page of the application"""
    return render_template('index.html', image='')


@app.route('/interactive', methods=['GET', 'POST'])
def return_interactive():
    if request.method == 'POST':
        file = request.files['fileToUpload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            MYDIR = os.path.dirname(__file__)
            file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(MYDIR + "/static", filename))
            dt = DecisionTree(max_depth=3)
            df = pd.read_csv(f'static/{filename}')
            target = list(df.columns)[-1]
            dt.fit(df, target)
            with open(f'static/json/{filename[0:-4]}.json', 'w') as fp:
                json.dump(dt.generate_json_like_structure_label(), fp)
            return render_template("interactive.html", json_name=f'json/{filename[0:-4]}.json')
    else:
        return render_template("index.html", info="No file uploaded", image='')


@app.route('/build', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        file = request.files['fileToUpload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            MYDIR = os.path.dirname(__file__)
            file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER'], filename))

            dt = DecisionTree(max_depth=3)
            df = pd.read_csv(f'static/{filename}')
            target = list(df.columns)[-1]
            dt.fit(df, target)
            dt.create_dot_png(f'static/img/{filename[0:-4]}')
            return render_template("index.html", image=f'img/{filename[0:-4]}.png')
    else:
        return render_template("index.html", info="No file uploaded", image='')


@app.route('/login')
def login():
    """Page for logging in"""
    return render_template('login.html')

@app.route('/register')
def register():
    """Page for registering"""
    return render_template('register.html')
application = app
if __name__ == '__main__':
    app.run(debug=True)
