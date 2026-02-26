from flask import Flask, render_template, request, redirect, url_for, session
import os
from utils import extract_text_from_pdf
from ranker import rank_resumes

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Automatically create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

USERNAME = "admin"
PASSWORD = "1234"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['admin'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        job_description = request.form['job_description']
        files = request.files.getlist('resumes')

        resumes = []
        for file in files:
            if file.filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)
                resumes.append((file.filename, text))

        ranked = rank_resumes(job_description, resumes)

        return render_template('results.html', ranked=ranked)

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)