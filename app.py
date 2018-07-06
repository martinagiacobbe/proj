from flask import Flask, render_template, request, json, url_for, redirect, send_from_directory
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import shutil
from keras.models import load_model
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
import cv2
import keras
from keras import backend as K
app = Flask(__name__)
#app = Flask(__name__, static_url_path='/static')

@app.route('/')
def main():
    pics = os.listdir('static/gallery/')
    return render_template('index.html', pics=pics,init=False,thepred=False)

@app.route('/show/<pic>')
def uploaded_file(pic):
    pics = os.listdir('static/gallery/')
    #shutil.copy('static/gallery/'+pic,TEST_FOLDER)
    return render_template('index.html',pics=pics, pic=pic, init=True,thepred=False)

#@app.route('/test/<pic>', methods=['GET'])
#def send_file(pic):
#    return send_from_directory('static/gallery/', pic, cache_timeout=1)

@app.route('/show/<pic>/button')
def button(pic):
    K.clear_session()
    pics = os.listdir('static/gallery/')
    path='static/gallery/'+pic
    img = load_img(path)
    x = img_to_array(img)*1.0/255
    xresized = cv2.resize(x, (128,128))
    inputarray = np.expand_dims(xresized, axis=0)
    loaded_model = keras.models.Sequential()
    loaded_model = load_model('nuovarete1.h5')
    cls = loaded_model.predict_classes(inputarray)
    prob=loaded_model.predict_proba(inputarray)
    explode = (0.05,0.05)
    labels = ['healty', 'ill']
    sizes = [1.0-prob[0,0],prob[0,0]]
    colors = ['#ff9999','#66b3ff']

    #fig1, ax1 = plt.subplots()
    #ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
    #centre_circle = plt.Circle((0,0),0.70,fc='white')
    #fig = plt.gcf()
    #fig.gca().add_artist(centre_circle)
    #ax1.axis('equal')
    #plt.tight_layout()
    #plt.show()
    #fig1.savefig('static/results/'+pic)
    #mpld3.fig_to_html(fig)
    return render_template('index.html', pics=pics, pic=pic, init=False, thepred=True, prob=prob,cls=cls) #url ='/static/results/'+pic)


if __name__=="__main__":
    app.run()
