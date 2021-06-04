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
    return render_template('index.html')


@app.route("/login",methods=['GET','POST'])
def login():
    msg = ''
    result = request.form
    if request.method == 'POST' and 'email' in result and 'password' in result and ('doctor-img' in result or 'patient-img' in result):
        if 'doctor-img' in result:
            doctor = 1
        else:
            doctor = 0
        email = result['email']
        password = result['password']
        cur = mysql.connection.cursor() #changing
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE email = %s AND password = %s AND doctor = %s', (email, password,doctor,))
        account = cur.fetchone() #check this, try to replace with TOP 1 in query
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['email'] = account[2]
            msg = 'Logged in successfully !\nWelcome, '+account[1]
            if doctor:
                msg = msg[:34]+'Dr. '+msg[34:]
            return render_template('login.html', msg=msg)  # return to patient/doctor .html
        else:
            msg = 'Incorrect username / password / Account Type !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    result = request.form
    if request.method == 'POST' and (result['password']!=result['rePassword']):
        msg = 'Password did not match'
    elif request.method == 'POST' and 'name' in result and 'password' in result and 'email' in result and 'morbidities' in result and ('doctor-img' in result or 'patient-img' in result):
        doctor = 0
        if 'doctor-img' in result:
            doctor = 1
        name = result['name']
        password = result['password']
        email = result['email']
        morbidities = result['morbidities']
        cur = mysql.connection.cursor()
        # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cur.fetchone() #check, replace with TOP 1 in query if needed
        if account:
            msg = 'Account already exists with this Email ID !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Username must contain only alphabets !'
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)',
                           (name, doctor, email, password, morbidities))
            mysql.connection.commit()
            cur.close()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg=msg)

@app.route("/about",methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route("/contact",methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route("/search",methods=['GET', 'POST'])
def search():
    msg = 'Search result empty'
    if request.method == 'GET':
        result = '"'+request.args.get('query')+'"'
        msg = "You have searched for "+ result
    return render_template('search.html',msg=msg)

