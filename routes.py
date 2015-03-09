
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from bs4 import BeautifulSoup
from flask import request as req
import requests as rq

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
        available = book[3]
        temp = available.split('/')
        
        arr1.append(int(temp[0]))
        arr2.append(int(temp[1]))


    for member in arr1:
        count1 += member


    for mbr in arr2:
        count2 += mbr

    availableBooks = count1

    total = count2

    return render_template('index.html', books=books, total=total, unique=unique, availableBooks=availableBooks)


@app.route('/request')
def request():
    return render_template('requestabook.html')
    
def add_entry():
    db.execute('insert into entries (title, text) values (? ?)',
                 [req.form['title'], req.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

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


@app.route('/netidcheck', methods=['POST', 'GET'])
def netidcheck():
    return render_template('netidcheck.html')

@app.route('/netidcheck/test', methods=['POST', 'GET'])
def netidchecktest():
    if req.method == 'POST':
        url = "https://illinois.edu/ds/search?skinId=0&sub=&go=go&search=%s&search_type=userid" % req.form['netid']
        r = rq.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        username = soup.find('h4', 'ws-ds-name detail-title').string
        print(username)
        role = soup.find('div', 'role-and-dept').contents[0].string
        if(not role):
            role = soup.find('div', 'ws-ds-title').string
    return render_template('netidtest.html', netid = username, position = role)

if __name__ == '__main__':
    app.run()