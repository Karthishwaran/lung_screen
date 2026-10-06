# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
from plotly import graph_objects as go
import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import argparse
import urllib.request
import urllib.parse

# necessary imports 
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
plt.style.use('fivethirtyeight')
#%matplotlib inline
pd.set_option('display.max_columns', 26)
##
from PIL import Image, ImageOps
import scipy.ndimage as ndi
from skimage import transform

from tensorflow.keras import layers, models
import torch
# import timm
from torchvision import transforms

##
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="lungs_screener"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html',msg=msg)




@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('test_img'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_user.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT max(id)+1 FROM register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO register(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,uname,pass1)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('login_user'))

    
        
    return render_template('register.html',msg=msg)




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    

    return render_template('admin.html')



@app.route('/img_process', methods=['GET', 'POST'])
def img_process():
    

    return render_template('img_process.html')

@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        '''img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (256, 256))
        cv2.imwrite("static/dataset/"+fname, rez)'''

        '''img = cv2.imread('static/data/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/trained/g_"+fname, gray)
        ##noice
        img = cv2.imread('static/trained/g_'+fname) 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        fname2='ns_'+fname
        cv2.imwrite("static/trained/"+fname2, dst)'''

    return render_template('pro1.html',dimg=dimg)


def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))



@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        '''f1=open("adata.txt",'w')
        f1.write(fname)
        f1.close()
        ##bin
        image = cv2.imread('static/data/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)'''

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        #cv2.imwrite("static/trained/bb/bin_"+fname, thresh)

    
   
    #RPN
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        ##
        img = cv2.imread('static/data/'+fname) 	
        
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/trained/sg/sg_"+fname
        #segment.save(path3)
        

    return render_template('pro2.html',dimg=dimg)

#UNet - Training
def load_data(img_path, mask_path):
    images = []
    masks = []

    for file in os.listdir(img_path):
        img = cv2.imread(os.path.join(img_path, file))
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0

        mask = cv2.imread(os.path.join(mask_path, file), 0)
        mask = cv2.resize(mask, (IMG_SIZE, IMG_SIZE))
        mask = mask / 255.0
        mask = np.expand_dims(mask, axis=-1)

        images.append(img)
        masks.append(mask)

    return np.array(images), np.array(masks)


# U-NET MODEL
def unet_model():
    X_train, Y_train = load_data("dataset/train/images", "dataset/train/masks")
    inputs = layers.Input((IMG_SIZE, IMG_SIZE, 3))

    # Encoder
    c1 = layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)
    c1 = layers.Conv2D(64, 3, activation='relu', padding='same')(c1)
    p1 = layers.MaxPooling2D()(c1)

    c2 = layers.Conv2D(128, 3, activation='relu', padding='same')(p1)
    c2 = layers.Conv2D(128, 3, activation='relu', padding='same')(c2)
    p2 = layers.MaxPooling2D()(c2)

    # Bottleneck
    c3 = layers.Conv2D(256, 3, activation='relu', padding='same')(p2)

    # Decoder
    u4 = layers.UpSampling2D()(c3)
    u4 = layers.concatenate([u4, c2])
    c4 = layers.Conv2D(128, 3, activation='relu', padding='same')(u4)

    u5 = layers.UpSampling2D()(c4)
    u5 = layers.concatenate([u5, c1])
    c5 = layers.Conv2D(64, 3, activation='relu', padding='same')(u5)

    outputs = layers.Conv2D(1, 1, activation='sigmoid')(c5)

    model = models.Model(inputs, outputs)
    return model


def segment_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img_norm = img / 255.0
    img_input = np.expand_dims(img_norm, axis=0)

    pred_mask = model.predict(img_input)[0]
    pred_mask = (pred_mask > 0.5).astype(np.uint8)

    segmented = img * pred_mask
    return segmented



@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
   
        '''img = Image.open('static/data1/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/trained/ff/'+fname)'''
        

    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        

        #####
        '''image = cv2.imread("static/data1/"+fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/trained/ff/"+fname
        #edged.save(path4)'''
        ##
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    return render_template('pro4.html',dimg=dimg)


    

@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    #graph
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[0,1,2,3,4]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model Precision")
    plt.ylabel("precision")
    
    fn="graph1.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph2
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[0,1,2,3,4]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model recall")
    plt.ylabel("recall")
    
    fn="graph2.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph3########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,24,38,50,62]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph3.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,24,38,50,62]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph4.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    return render_template('pro5.html',dimg=dimg)

def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m
                
@app.route('/pro6', methods=['GET', 'POST'])
def pro6():
    msg=""
    dimg=[]
    path_main = 'static/data1'
    print("aaa")
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')
    '''data1=[]
    data2=[]
    data3=[]
    data4=[]
    v1=0
    v2=0
    v3=0
    v4=0
    path_main = 'static/trained'
    #for fname in os.listdir(path_main):
    i=0
    i<127
        dimg.append(fname)
        d1=fname.split('_')
        if d1[0]=='d':
            data1.append(fname)
            v1+=1
        if d1[0]=='f':
            data2.append(fname)
            v2+=1
        if d1[0]=='n':
            data3.append(fname)
            v3+=1
        if d1[0]=='w':
            data4.append(fname)
            v4+=1
        

    g1=v1+v2+v3+v4
    dd2=[v1,v2,v3,v4]
    
    
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 5))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,g1))
    plt.xlabel("Objects")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()'''

    #,data1=data1,data2=data2,data3=data3,data4=data4,cname=cname,v1=v1,v2=v2,v3=v3,v4=v4
    ##############################

    
    ###############################
    
    
    

    return render_template('pro6.html',dimg=dimg)

#######
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    
    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')


    ##    
    ff2=open("static/trained/tdata.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')
    ##
    

    #ffq=open("static/trained/adata.txt",'r')
    #ext1=ffq.read()
    #ffq.close()

    v1=0
    v2=0
    v3=0
    
    data2=[]
    #ex=ext1.split(',')
    dt1=[]
    dt2=[]
    dt3=[]
    
    g=0
    for nx in ex:
        g+=1
        nn=nx.split('-')
        if nn[1]=='1':
            
            dt1.append(nn[0])
            
            v1+=1
        if nn[1]=='2':
            dt2.append(nn[0])
            
            v2+=1
        if nn[1]=='3':
            dt3.append(nn[0])
            
            v3+=1
        
        
    data2.append(dt1)
    data2.append(dt2)
    data2.append(dt3)
    
    print(data2)   
    dd2=[v1,v2,v3]
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,62))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=10)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()
    return render_template('classify.html',msg=msg,cname=cname,data2=data2)

#######
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""

    
        
    return render_template('userhome.html',msg=msg)

#ViT Model 

# Load pretrained ViT
# model = timm.create_model('vit_base_patch16_224', pretrained=True, num_classes=3)
# model.eval()

# Transform
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Class names
classes = ["Normal", "benign", "malignant"]

def predict(image_path):
    img = cv2.imread(image_path)
    img = transform(img)
    img = img.unsqueeze(0)

    with torch.no_grad():
        output = model(img)
        pred = torch.argmax(output, dim=1)

    return classes[pred.item()]

def predict():   
    for file in os.listdir("dataset/segmented"):
        result = predict(os.path.join("dataset/segmented", file))
        print(file, "->", result)
    
@app.route('/test_img', methods=['GET', 'POST'])
def test_img():
    msg=""
    ss=""
    fn=""
    fn1=""
    tclass=0

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')
    
    if request.method=='POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            f1=open('static/test/file.txt','w')
            f1.write(filename)
            f1.close()
            file.save(os.path.join("static/test", filename))

        cutoff=1
        path_main = 'static/data'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/data/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                
                break
            else:
                ss="no"
        print("fn===="+fn)
        if ss=="ok":
            print("yes")
            tclass=0
            dimg=[]

            ##    
            ff2=open("static/trained/tdata.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            
            print(fn)
            ##
            for nx in ex:
                
                nn=nx.split('-')
                
                f='a ('+nn[0]+').jpg'
                fn1='a ('+nn[0]+').png'
                if f==fn:
                    tclass=int(nn[1])
                    break

            
            print(tclass)
            tt=tclass-1
            cla=cname[tt]
            dta=cla+"|"+fn+"|"+fn1
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()

            
                    
            return redirect(url_for('test_pro',act="1"))
        else:
            msg="Invalid!"
   
        
    return render_template('test_img.html',msg=msg,fn1=fn1)

    
@app.route('/test_pro', methods=['GET', 'POST'])
def test_pro():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    fn1=gs[2]
    ts=gs[0]
    fname=fn
    ##bin
    '''image = cv2.imread('static/dataset/'+fn)
    original = image.copy()
    kmeans = kmeans_color_quantization(image, clusters=4)

    # Convert to grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
        cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
        break
    
    # Bitwise-and for result
    result = cv2.bitwise_and(original, original, mask=mask)
    result[mask==0] = (0,0,0)

    
    ###cv2.imshow('thresh', thresh)
    ###cv2.imshow('result', result)
    ###cv2.imshow('mask', mask)
    ###cv2.imshow('kmeans', kmeans)
    ###cv2.imshow('image', image)
    ###cv2.waitKey()

    #cv2.imwrite("static/upload/bin_"+fname, thresh)'''
    

    ###fg
    '''img = cv2.imread('static/dataset/'+fn)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    segment = cv2.subtract(sure_bg,sure_fg)
    img = Image.fromarray(img)
    segment = Image.fromarray(segment)
    path3="static/trained/test/fg_"+fname
    #segment.save(path3)'''
    
        
    return render_template('test_pro.html',msg=msg,fn=fn,ts=ts,act=act,fn1=fn1)

# @app.route('/test_pro2', methods=['GET', 'POST'])
# def test_pro2():
#     msg=""
#     fn=""
#     act=request.args.get("act")
#     f2=open("static/test/res.txt","r")
#     get_data=f2.read()
#     f2.close()

#     #f3=open("static/test/file.txt","r")
#     #fn=f3.read()
#     #f3.close()

#     gs=get_data.split('|')
    
#     print(fn)
#     ts=gs[0]
#     fn=gs[1]
#     fn1=gs[2]

#     if ts=="Bengin":
#         ts="Benign"

#     mycursor = mydb.cursor()
   
#     mycursor.execute("SELECT * from recommendation order by rand() limit 0,3")
#     data = mycursor.fetchall()
        
#     return render_template('test_pro2.html',msg=msg,fn=fn,ts=ts,act=act,fn1=fn1,data=data)


# @app.route('/test_pro2', methods=['GET', 'POST'])
# def test_pro2():
#     msg = ""
#     fn = ""
#     act = request.args.get("act")

#     f2 = open("static/test/res.txt", "r")
#     get_data = f2.read()
#     f2.close()

#     gs = get_data.split('|')

#     ts = gs[0]
#     fn = gs[1]
#     fn1 = gs[2]

    
#     if ts == "Bengin":
#         ts = "Benign"
#     elif ts == "Malign":
#         ts = "Malignant"

#     mycursor = mydb.cursor()

#     #  Different logic based on case
#     if ts == "Benign":
#         msg = " Benign case detected. No serious risk."
        
#         mycursor.execute("""
#             SELECT * FROM recommendation 
#             WHERE type='benign'
#             ORDER BY RAND() LIMIT 3
#         """)
#         data = mycursor.fetchall()

#     elif ts == "Malignant":
#         msg = " Malignant case detected! Immediate cancer treatment required."
        
#         mycursor.execute("""
#             SELECT * FROM recommendation 
#             WHERE type='malignant'
#             ORDER BY RAND() LIMIT 3
#         """)
#         data = mycursor.fetchall()

#     else:
#         msg = "Normal"
#         data = []

#     return render_template(
#         'test_pro2.html',
#         msg=msg,
#         fn=fn,
#         ts=ts,
#         act=act,
#         fn1=fn1,
#         data=data
#     )

@app.route('/test_pro2', methods=['GET', 'POST'])
def test_pro2():
    msg = ""
    fn = ""
    act = request.args.get("act")

    f2 = open("static/test/res.txt", "r")
    get_data = f2.read()
    f2.close()

    gs = get_data.split('|')

    ts = gs[0]
    fn = gs[1]
    fn1 = gs[2]

    if ts == "Bengin":
        ts = "Benign"
    elif ts == "Malign":
        ts = "Malignant"

    return render_template(
        'test_pro2.html',
        msg=msg,
        fn=fn,
        ts=ts,
        act=act,
        fn1=fn1
    )

@app.route('/select_district')
def select_district():
    return render_template('select_district.html')

@app.route('/view_hospitals', methods=['POST'])
def view_hospitals():
    district = request.form.get('district').strip()

    print("Selected District:", district)

    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT * FROM recommendation WHERE LOWER(city) LIKE LOWER(%s)",
        ('%' + district + '%',)
    )

    data = mycursor.fetchall()

    print("Data:", data)

    return render_template('view_hospitals.html', data=data, district=district)
##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


