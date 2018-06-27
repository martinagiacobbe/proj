from flask import Flask, render_template, request, json, url_for, redirect, send_from_directory
import os
from keras.models import load_model
#from flaskext.mysql  import MySQL
app = Flask(__name__)
#app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    #file.filename
    filename='photo.jpg'
    f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)
    
    return redirect(url_for('uploaded_file', filename=filename))

@app.route('/show/<filename>')
def uploaded_file(filename):
    return render_template('index.html', filename=filename, init=True)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, cache_timeout = 1)


@app.route('/retry', methods=["GET", "POST"])
def retry():
    return render_template('index.html', init=False)


def load_model():
    loaded_model = load_model('nuovarete1.h5')
    loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    score = loaded_model.evaluate_generator(test_generator)
    return("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

if __name__=="__main__":
    app.run()
