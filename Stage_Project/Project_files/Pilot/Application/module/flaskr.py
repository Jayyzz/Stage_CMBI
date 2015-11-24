# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
#from flask_debugtoolbar import DebugToolbarExtension
from contextlib import closing

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

# creating the application
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#toolbar = DebugToolbarExtension(app)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

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
def show_entries():
    cur = g.db.execute('select title, text, score, id from entries order by score desc')
    entries = [dict(title=row[0], text=row[1], score=row[2], id=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/create', methods=['GET', 'POST'])
def create_entry():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into entries (title, text, score) values (?, ?, 0)',
                     [request.form['title'], request.form['text']])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries.html'))
    return render_template('create_entry.html')

@app.route('/upvote/<ID>')
def upvote(ID):
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('update entries set score=(score+1) where id = ?',[ID])
    g.db.commit()
    flash('This post is now upvoted!')
    return redirect(url_for('show_entries'))

        

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        c = g.db.execute('select user, password from users where user= ?', [request.form['username']])
        user = c.fetchone()
        username = user[0]
        password = user[1]
        
        if  user is None:
            error = 'Invalid username'
        elif password != request.form['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] == g.db.execute('select user from users'):
            error = 'Username is already used.'
        elif request.form['password'] != request.form['confirm']:
            error = "Passwords don't match."
        else:
            g.db.execute('insert into users(user, password) values (?, ?)',
                     [request.form['username'], request.form['password']])
            g.db.commit()
            session['logged_in'] = True
            flash('You have registered and you are now logged in')
            return redirect(url_for('show_entries'))
        return render_template('register.html', error=error)
    return render_template('register.html', error=error)    

                                                      
if __name__ == '__main__':
    app.run()
