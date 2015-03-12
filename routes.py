# all the imports
import sqlite3
from flask import Flask, jsonify, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from bs4 import BeautifulSoup
from flask import request 
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
    unique = db.execute('SELECT COUNT(name) FROM books')
    unique = unique.fetchall()[0][0]
    books = cur.fetchall()

    arr1=[]
    arr2=[]
    count1 = 0
    count2 = 0

    for book in books:
        available = book['available']
        copies = book['copies']
        
        arr1.append(available)
        arr2.append(copies)


    for member in arr1:
        count1 += member


    for mbr in arr2:
        count2 += mbr

    availableBooks = count1
    copies = count2
    checkedOut = copies - availableBooks
    return render_template('index.html', books=books, unique=unique, copies=copies, availableBooks=availableBooks, checkedOut=checkedOut)


@app.route('/request', methods = ['POST', 'GET'])
def showrequests():
    db = get_db()
    cur = db.execute('select bookname, category, author from requests')
    requests = [dict(bookname=row[0], category=row[1], author=row[2]) for row in cur.fetchall()]
    return render_template('requestabook.html', requests = requests)

@app.route('/request/book', methods = ['POST', 'GET'])
def requestbook():
    if request.method == 'POST':
        g.db.execute('insert into requests(bookname, category, author) values (?, ?, ?)', [request.form['bookname'], request.form['categories'], request.form['author']])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('showrequests'))

'''@app.route('/request/show')
def showrequests():
    db = get_db()
    cur = db.execute('select bookname, category, author from requests')
    requests = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('requestedbooks.html', requests = requests)'''

@app.route('/overdue')
def overdue():
    return render_template('overdue.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    flash('Blah.')
    if req.method == 'POST':
        if req.form['netid'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif req.form['password'] != app.config['PASSWORD']:
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


@app.route('/booklookup')
def booklookup():
    return render_template('booklookup.html');

@app.route('/booklookup/apicall', methods=['POST'])
def booklookupapicall():
    book_name = req.form['bookname']
    query_args = {'q': book_name}
    encoded_args = urllib.urlencode(query_args)
    print(encoded_args)
    url = 'https://www.googleapis.com/books/v1/volumes?' + encoded_args
    response = urllib2.urlopen(url)
    data = json.load(response)
    return jsonify(data)

@app.route('/netidcheck', methods=['POST', 'GET'])
def netidcheck():
    return render_template('netidcheck.html')

@app.route('/netidcheck/test', methods=['POST'])
def netidchecktest():
    url = "https://illinois.edu/ds/search?skinId=0&sub=&go=go&search=%s&search_type=userid" % req.form['netid']
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