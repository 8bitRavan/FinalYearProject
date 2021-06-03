from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
#import MySQLdb.cursors
import re
import os

secKey = os.environ['SECKEY']
mysqlPass = os.environ['MYSQLPswd']
app = Flask(__name__)

app.secret_key = secKey

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = mysqlPass
app.config['MYSQL_DB'] = 'userdb'

mysql = MySQL(app)


@app.route("/")
def index():
    x = "<a href='/login'>Click</a>"
    return (x)


@app.route("/login")
def login():
    msg = ''
    if 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor() #changing
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM patient_accounts WHERE email = %s AND password = %s', (email, password,))
        account = cur.fetchone() #check this, try to replace with TOP 1 in query
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('login.html', msg=msg)  # return to patient/doctor .html
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route("/result", methods=['GET','POST'])
def result():
    return ('nothing')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'morbidities' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        morbidities = request.form['morbidities']
        cur = mysql.connection.cursor()
        # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM patient_accounts WHERE email = %s', (email))
        account = cur.fetchone() #check, replace with TOP 1 in query if needed
        if account:
            msg = 'Account already exists with this Email ID !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Username must contain only alphabets !'
        else:
            cur.execute('INSERT INTO patient_accounts VALUES (NULL, %s, %s, %s, %s)',
                           (name, email, password, morbidities))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg=msg)

