# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
from contextlib import closing
import os
import sys

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

if __name__ == '__main__':
    app.run()

