from flask import Flask, render_template, request, json, url_for, redirect, send_from_directory
import os
import shutil
from keras.models import load_model
import numpy as np
import cv2
from keras.preprocessing.image import img_to_array, load_img
import keras
from keras import backend as K
from collections import Counter
from math import pi
import pandas as pd

from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.embed import components

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
    
    return render_template('index.html', _anchor="load", controllo_load="load", pics=pics, pic=pic, init=True,thepred=False)

#@app.route('/test/<pic>', methods=['GET'])
#def send_file(pic):
#    return send_from_directory('static/gallery/', pic, cache_timeout=1)

def bokeh_plt(pic, sizes, labels):
    sizes=[int(round(sizes[0]*100)),sizes[1]*100]
    print(sizes)
    sizes=[sizes[0],100-sizes[0]]
    print(sizes)
    output_file("pie.html")
    dic=dict(zip(labels,sizes))
    x = Counter(dic)
    
    data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0:'value', 'index':'type'})
    
    data['angle'] = data['value']/sum(x.values()) * 2*pi
    data['color'] = [Category20c[len(x)+15][13]]+[Category20c[len(x)+8][2]]
    print(data)
    
    data['value'] = data['value'].astype('str')
    data['value']=data['value']+['%']*len(data['value'])
    p = figure(plot_height=350, toolbar_location=None,
               tools="hover", tooltips="@type: @value")
    p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='type', source=data)
               
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    return p



@app.route('/show/<pic>/button')
def button(pic):
    pics = os.listdir('static/gallery/')
    K.clear_session()
    pics = os.listdir('static/gallery/')
    path='static/gallery/'+pic
    img=img = cv2.imread(path)
    x = img_to_array(img)*1.0/255
    xresized = cv2.resize(x, (128,128))
    inputarray = np.expand_dims(xresized, axis=0)
    loaded_model = keras.models.Sequential()
    loaded_model = load_model('nuovarete1.h5')
    cls = loaded_model.predict_classes(inputarray)
    prob=loaded_model.predict_proba(inputarray)
    labels = ['HEALTHY', 'ILL']
    sizes = [1.0-prob[0,0],prob[0,0]]
    print(sizes)
    p=bokeh_plt(pic,sizes,labels)
    script, div = components(p)
    return render_template('index.html', _anchor='pred', pics=pics, pic=pic, init=False, thepred='pred', prob=prob, cls=cls, script=script, div=div)

if __name__=="__main__":
    app.run()
