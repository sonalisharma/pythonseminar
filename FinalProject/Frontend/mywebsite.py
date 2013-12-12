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
from sklearn.cross_validation import cross_val_score
import pickle

FILENAME ="newdata_1200.csv"
DATA = pd.read_csv("../Notebooks/Data/"+FILENAME,sep = "\t",header=0)
DATA = DATA.fillna(0)
data_features = pd.read_csv("../Notebooks/Finaldata/features.csv",sep = ",",header=0)
data_target = pd.read_csv("../Notebooks/Finaldata/target.csv",sep = ",",header=0)
print len(data_target)
print len(data_features)

app = Flask(__name__)

db = SQLAlchemy(app)
eng = db.create_engine("sqlite:///crowdfunding.db")
#db.drop_all()
db.create_all()
app.debug = True


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
    score = print_cv_score_summary(clf,data_features.values,data_target.values,cv=cross_validation.KFold(len(data_target), 10))
    features = data_features.columns
    print features
    #features = ["Count_comment","Count_funder", "Count_photo", "Mintotal", "Maxtotal", "Mediantotal"]
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


def getcountries():
    countries = list(DATA['Country'].unique())
    return countries

def getresult(userinput):
    pkl_file = open("classifier_new.p", 'rb')
    clf = pickle.load(pkl_file)
    X = np.array(userinput)
    print X
    X_scaled = preprocessing.scale(X)
    preds = clf.predict(X_scaled)
    print preds
    if preds == 1:
        status = "Successful"
    if preds == 2:
        status = "Moderately Successful"
    if preds == 3:
        status = "UnSuccessful"
    return status

def gettitle(plotname):
    plot = {"Count_update":["No. of updates",40],
    "Count_comment":["No. of comments",200], 
    "Count_funder":["No. of Funders",500],
    "Count_photo":["No. of photos uploaded",60], 
    "Amount_goal":["Amount to be raised",1000000] ,
    "Start_month": ["Project start month",12],
    "End_month": ["Project end month",12],
    "Duration":["Duration of Project",150], 
    "Min_perk":["Amount of minimum perk($)",200], 
    "No_min_perk":["No. of people contributing to min perk",100], 
    "Max_perk":["Amount of maximum perk($)",50000], 
    "No_max_perk":["No. of people contributing to max perk",50], 
    "Median_perk":["Amount of median perk($)",2000], 
    "No_med_perk":["No. of people contributing to median perk",100], 
    "Total_perk":["Total perks given",22], 
    "FB_like":["Total FB likes",3000], 
    "FB_talking":["Total FB shares",3000], 
    "Youtube_avg_duratio":["Youtube video duration",2000], 
    "Youtube_avg_view_count":["Youtube video count",5000000], 
    "Youtube_avg_rating":["Youtube video avg ratings",6], 
    "Mintotal":["Total money raised by min perk",50000], 
    "Maxtotal":["Total money raised by max perk",20000]}
    return plot.get(plotname)

def drawplot(name,radio):
    print radio
    g_data = gettitle(name)
    print "This is it"
    print g_data
    cols = {1: "blue", 2: "green", 3: "red"}
    label = {1}
    xaxis = data_features[name]
    amount_raised = DATA['Amount_Raised']
    color = map(lambda x: cols[x],data_target['target'])
    print "=================="
    print str(str(radio[0]))
    print "=================="
    if (str(str(radio[0]))=="small"):
        print "small is here"
        fig,ax1 = plt.subplots(figsize=(8,6))
    else:
        print "large is here"
        fig,ax1 = plt.subplots(figsize=(12,10))

    ax1.scatter(xaxis,amount_raised,c = color, lw = 0.5)
    ax1.set_title(g_data[0])    
    ax1.set_xlabel(name)
    ax1.set_ylabel('Amount Raised')
    ax1.set_ylim([0,50000])
    ax1.set_xlim([-5,g_data[1]])
    line1 = plt.Line2D(range(1), range(1), color="white", marker='o', markerfacecolor="blue")
    line2 = plt.Line2D(range(1), range(1), color="white", marker='o',markerfacecolor="green")
    line3 = plt.Line2D(range(1), range(1), color="white", marker='o',markersize=5, markerfacecolor="red")
    plt.legend((line1,line2,line3),('Succesful','Moderately Successful', 'Unsuccessful'),numpoints=1, loc=1)
    filepath = "static/img/Plots/"+name+".png"
    try:
        os.remove("static/img/Plots/"+name+".png")
    except:
        print "Did not file an existing file to delete"
    fig.savefig(filepath) 
    return  filepath


@app.route('/data', methods=['GET', 'POST'])
def data():
    datajson = json.loads(request.form.get('data'))
    print datajson
    vhtml = "<ul class=\"entries\">"
    data = datajson['value']
    print "#################"
    print data
    print "#################"
    for d in data:
        print "I am here this is "+d
        filepath = drawplot(d,datajson['radio'])
        vhtml =vhtml+"<li><img style=\"zoom: 0.5\" src=\""+filepath+"\"/></li>"
    vhtml = vhtml+"</ul>"
    return vhtml


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    countries = getcountries()
    predict = None
    user_input = []
    if request.method == 'POST':
        #try:
        comment_cnt = request.form["count_comment"]
        amount_goal = request.form["amount_goal"]
        funder_cnt = request.form["count_funder"]
        photo_cnt = request.form["count_photo"]
        min_perk = request.form["min_perk"]
        max_perk = request.form["max_perk"]
        no_min_perk = request.form["no_min_perk"]
        no_max_perk = request.form["no_max_perk"]
        user_input = [float(amount_goal),float(comment_cnt),float(funder_cnt),
        float(photo_cnt),float(min_perk),float(no_min_perk),float(max_perk),float(no_max_perk)]


        predict = getresult([float(comment_cnt),float(amount_goal),float(funder_cnt),
        float(photo_cnt),float(min_perk)*float(no_min_perk),float(max_perk)*float(no_max_perk)])
        print predict
        return render_template('predict.html',countries=countries,prediction=predict,userinput=user_input)
        #except:
        #print "Exception occurred"
    return render_template('predict.html',countries=countries,prediction=predict,userinput=user_input)

if __name__ == "__main__":
    app.run()

