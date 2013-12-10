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

FILENAME ="newdata_1200.csv"
DATA = pd.read_csv("../Notebooks/Data/"+FILENAME,sep = "\t",header=0)

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

