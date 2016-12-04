import bibtexparser
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['bib', 'bibtex', 'tex'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/new', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return(redirect(url_for('view',
                                    filename=filename)))
    return render_template("upload.html")




@app.route('/view/<filename>')
def view(filename):
    with open('uploads/{}'.format(filename)) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    d = bib_database.entries
    return(render_template('main.html', result = d, filename = filename))



if __name__ == '__main__':
   app.run(debug = True)
