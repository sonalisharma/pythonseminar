import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for
from flask import send_from_directory   
from pybtex.database.input import bibtex
from sqlalchemy import distinct
from itertools import izip


UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['bib'])


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibtex.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
eng = db.create_engine("sqlite:///bibtex.db")
db.drop_all()
db.create_all()
app.debug = True


class Bibparse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100))
    type = db.Column(db.String(1500))
    author = db.Column(db.String(1500))
    journal = db.Column(db.String(1500))
    keywords = db.Column(db.String(1500))
    pages = db.Column(db.String(1500))
    title = db.Column(db.String(1500))
    volume = db.Column(db.Integer)
    year = db.Column(db.Integer)
    collection_name = db.Column(db.String(120))

    def __init__(self, uniqueidentifier, type,author,journal,keywords,pages,title,volume,year,collectionname):
        self.tag = uniqueidentifier
        self.type = type
        self.author = author
        self.journal = journal
        self.keywords = keywords
        self.pages = pages
        self.title = title
        self.volume = volume
        self.year = year
        self.collection_name = collectionname


    def __repr__(self):
        return 'Yo, my name is %r' % self.author

@app.route("/")
def get_file():
    collections = db.session.query(distinct(Bibparse.collection_name)).all()
    return render_template('index.html',answer = collections)

    #print " ".join([str(x) for x in User.query.all()])
    #repreturn repr([x.email for x in User.query.all()])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload_file" , methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        colname = request.form['txt_collectionname']
        print colname
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename,collectionname=str(colname)))
    return render_template('collections.html')
    #user = User(request.form['username'], request.form['message'])
    #admin = User.query.filter_by(username='admin').first()
@app.route('/uploads/<filename>/<collectionname>', methods=['GET', 'POST'])
def uploaded_file(filename,collectionname=None):
    flag = "success"
    try:
        parser = bibtex.Parser()
        bib_data = parser.parse_file('temp/'+filename)
        #enteries = ['id','type','author','journal','keywords','pages','title','volume','year','collectionname']
        enteries = ['author','journal','keywords','pages','title','volume','year']
        data = [] 

        for k in bib_data.entries.keys():
            data.append(k)
            print k
            data.append(bib_data.entries[k].type)
            for e in enteries:
                try:
                    data.append(bib_data.entries[k].fields[e])
                except:
                    data.append("Not available")
            data.append(collectionname)
            print "------------------------------------------"
            print data[0]
            print "------------------------------------------"
            bibdata = Bibparse(str(data[0]),str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[5]),str(data[6])
               ,data[7],data[8],str(data[9]))
            db.session.add(bibdata)
            db.session.commit()
    except Exception,e:
        flag = "failure"
        print e

        #return redirect(url_for('message', username=bibdata.username))
    #user = Bibparse.query.filter_by(collectionname="astronomy").first_or_404()
    return redirect(url_for('results',output=flag, collectionname=collectionname))
    #peter = Bibparse.query.filter_by(collectionname='astronomy').first()
    #return peter.author
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
                               #filename)
@app.route('/result/<output>/<collectionname>')
def results(output,collectionname):
    if (output == "success"):
        message = "Congratulations! you uploaded your collection."
    else:
        message = "Oops! Looks like soemthing went wrong, try again!"
    #user = User(request.form['username'], request.form['message'])
    #admin = User.query.filter_by(username='admin').first()
    return render_template('status.html',status = message, collectionname= collectionname)

@app.route("/query", methods=['GET', 'POST'])
def run_query():
    query_template=""
    results = ""
    final_data=[]
    if request.method == 'POST':
        query = request.form['txt_querystring']
        collectionname = request.form['txt_collectionname']
        if collectionname:
            query = query + " and collection_name="+str("\'"+collectionname+"\'")
        print query
        query_template = "select * from Bibparse WHERE {}".format(query)
        con =  eng.connect()
        try:
            results = con.execute(query_template)
            #data = db.session.query(Bibparse.collectionname = collectionname)
            headers = ["id","Tag","Type","Author","Journal","Keywords","Pages","Title","Volume",
            "Year","Collection Name"]
            for data in results:
                final_data.append([row for row in izip(headers,data)])
            print final_data
            return render_template("query.html",query = query_template, results = final_data,status="success")
        except:
            return render_template("query.html",query = query_template, results = final_data,status="failure")
    return render_template("query.html",query = query_template, results = results,status="success")
    

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run()

