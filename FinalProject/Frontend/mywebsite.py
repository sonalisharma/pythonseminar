import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from flask import Flask, request, redirect, url_for
from itertools import izip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn import neighbors
from sklearn import preprocessing
import json
from sklearn import cross_validation
from sklearn import linear_model
clf = linear_model.LogisticRegression()
from sklearn.cross_validation import cross_val_score

FILENAME ="newdata_1200.csv"
DATA = pd.read_csv("../Notebooks/Data/"+FILENAME,sep = "\t",header=0)
DATA = DATA.fillna(0)
data_features = pd.read_csv("../Notebooks/Finaldata/features.csv",sep = ",",header=0)

data_target = pd.read_csv("../Notebooks/Finaldata/target.csv",sep = ",",header=0)
print data_target

app = Flask(__name__)

db = SQLAlchemy(app)
eng = db.create_engine("sqlite:///crowdfunding.db")
#db.drop_all()
db.create_all()
app.debug = True


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(1500))
    pin = db.Column(db.String(1500))
    follow = db.Column(db.Integer)
    matchpin = db.Column(db.String(1500))
    expressinterest = db.Column(db.String(1500))
    answer = db.Column(db.String(1500))
    email = db.Column(db.String(1500))

    def __init__(self, name, status,pin,follow,matchpin,expressinterest,answer,email):
        self.name = name
        self.status = status
        self.pin = pin
        self.follow = follow
        self.matchpin = matchpin
        self.expressinterest = expressinterest
        self.answer = answer
        self.email = email

    def __repr__(self):
        return 'Yo, my name is %r' % self.name

@app.route("/", methods=['GET', 'POST'])
def summary():
    if request.method == 'POST':
        pass
    return render_template('main.html')

def print_cv_score_summary(model, xx, yy, cv):
    scores = cross_val_score(model, xx, yy, cv=cv, n_jobs=1)
    print ("mean: {:3f}, stdev: {:3f}".format(
        np.mean(scores), np.std(scores)))
    return("{:3f},{:3f}".format(
        np.mean(scores), np.std(scores)))

@app.route("/analyse")
def analyse():
    clf = linear_model.LogisticRegression()
    score = print_cv_score_summary(clf,data_features.values,data_target,cv=cross_validation.KFold(len(data_target), 10))
    features = data_features.columns
    return render_template('analyse.html',score=score,features=features)

def setstatus(ratio):
    if (ratio>=1):
        return 1
    if (ratio>=0.66 and ratio <1):
        return 2
    if (ratio<0.66):
        return 3

def getstatus(data):
    data['status'] = data['Ratio'].apply(setstatus)
    ratio = data['Ratio']
    return ratio

@app.route('/analysis')
def fetchdata():
    #users = getusers
    return render_template('makematch.html')

def getcountries():
    countries = list(DATA['County'].unique())
    return countries

def getresult():
    return "Unsuccessful"

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    countries = getcountries()
    predict = None
    if request.method == 'POST':
        country = request.form["countries"]
        no_of_funders = request.form["no_of_funders"]
        max_perk = request.form["max_perk"]
        min_perk = request.form["min_perk"]
        total_perks = request.form["total_perks"]
        fb_like = request.form["fb_like"]
        fundtype = request.form["type"] 
        print country,no_of_funders,max_perk,min_perk,total_perks,fb_like,fundtype
        predict = getresult()
        print predict
        return render_template('predict.html',countries=countries,prediction=predict)
    return render_template('predict.html',countries=countries,prediction=predict)


if __name__ == "__main__":
    global name
    global email
    global radio
    global colorbox
    #db.drop_all()
    #db.create_all()
    app.run()

