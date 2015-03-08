# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from contextlib import closing
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

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar("FLASKR_SETTINGS", silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('select * from books')
    counter = db.execute('SELECT COUNT(name) FROM books')
    counter = counter.fetchall()[0][0]
    books = cur.fetchall()
    return render_template('index.html', books=books, counter=counter)

@app.route('/overdue')
def overdue():
    return render_template('overdue.html')

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
