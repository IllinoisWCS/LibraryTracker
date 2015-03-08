# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
<<<<<<< HEAD
     abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
=======
     abort, render_template, flash, jsonify
>>>>>>> netid
from contextlib import closing
import os
import sys
from bs4 import BeautifulSoup
import requests as rq
import urllib2
import urllib
import json


# configuration
DATABASE = 'LibraryTracker.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://wcs:wcssuperawesomepassword@localhost:15432/librarytracker')

# create our little application :)
app = Flask(__name__)
app.logger.info('SQLALCHEMY_DATABASE_URI: %s', SQLALCHEMY_DATABASE_URI)
db = SQLAlchemy(app)
app.config.from_object(__name__)

app.config.from_envvar("FLASKR_SETTINGS", silent=True)

@app.before_first_request
def before_first_request():
    app.logger.info('Creating Database Tables...')
    try:
        db.create_all()
        app.logger.info('Database Tables Created!')
    except Exception, e:
        app.logger.error('There was an error connecting or creating the tables in the database. Terminating...\n %s', e)
        sys.exit(1)


@app.route('/request', methods=['POST'])
def request():
    return render_template('requestabook.html')
    
def add_entry():
    g.db.execute('insert into entries (title, text) values (? ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/')
def index():
    books = Book.query.all()
    people = Person.query.all()
    counter = Book.query.count()
    return render_template('index.html', books=books, counter=counter)

@app.route('/overdue')
def overdue():
    return render_template('overdue.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    flash('Blah.')
    if request.method == 'POST':
        if request.form['netid'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            flash('Blah 2.')
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('base'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('base.html'))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(8), index=True, unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<Person %r>' % (self.netid)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    authors = db.Column(db.String(120))
    available = db.Column(db.String(120))
    cover = db.Column(db.String(120))
    year = db.Column(db.Integer)

    def __repr__(self):
        return '<Book %r>' % (self.name)

@app.route('/booklookup')
def booklookup():
    return render_template('booklookup.html');

@app.route('/booklookup/apicall', methods=['POST'])
def booklookupapicall():
    book_name = request.form['bookname']
    query_args = {'q': book_name}
    encoded_args = urllib.urlencode(query_args)
    print(encoded_args)
    url = 'https://www.googleapis.com/books/v1/volumes?' + encoded_args
    response = urllib2.urlopen(url)
    data = json.load(response)
    #print json.dumps(data, indent=4, sort_keys=True)
    print data['items'][0]['volumeInfo']['industryIdentifiers'][0]
    return jsonify(data)

@app.route('/netidcheck', methods=['POST', 'GET'])
def netidcheck():
    return render_template('netidcheck.html')

@app.route('/netidcheck/test', methods=['POST'])
def netidchecktest():

    url = "https://illinois.edu/ds/search?skinId=0&sub=&go=go&search=%s&search_type=userid" % request.form['netid']
    r = rq.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    username = soup.find('h4', 'ws-ds-name detail-title').string
    role = soup.find('div', 'role-and-dept').contents[0].string
    if(not role):
        role = soup.find('div', 'ws-ds-title').string
        return "Welcome! " + username
    return "Hello, " + role + " " + username

if __name__ == '__main__':
    app.run()

