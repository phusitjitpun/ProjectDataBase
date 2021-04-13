from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import random
from datetime import date
import datetime
from sqlalchemy import Column,Integer,String,Date 
import re
import http.client
import mimetypes



app = Flask(__name__)
app.secret_key = 'how_to_be_got_A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:BFCqhr46914@node4943-env-2254395.th.app.ruk-com.cloud:5432/pythonlogin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    user_id = 0
    email = ""
    newpass =""
    recode =''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = psycopg2.connect(user="webadmin",
                                password="BFCqhr46914", 
                                host="node4943-env-2254395.th.app.ruk-com.cloud", 
                                port="5432", 
                                database="pythonlogin")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchall()
        for row in account:
            user_id += row[0]
            email += row[3]
            recode += row[4]
        if account:
            session['loggedin'] = True
            session['user_id'] = user_id
            #session['username'] = account['username']
            for i in password:
                i = '*'
                newpass += i
            session['password'] = newpass
            session['username'] = username
            session['email'] = email
            session['code_repassword'] = recode
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)



@app.route('/pythonlogin/table')#ทองโลก
def table():
    if 'loggedin' in session:
        connection = psycopg2.connect(user="webadmin",
                                password="BFCqhr46914", 
                                host="node4943-env-2254395.th.app.ruk-com.cloud", 
                                port="5432", 
                                database="pythonlogin")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM GoldAPI ')
        Gold_records = cursor.fetchall()
        Gold_records = Gold_records[::-1]
        return render_template("table.html", value=Gold_records) 
    return redirect(url_for('table'))



@app.route('/pythonlogin/tableTH')#เงินบาท
def tableTH():
    if 'loggedin' in session:
        connection = psycopg2.connect(user="webadmin",
                                password="BFCqhr46914", 
                                host="node4943-env-2254395.th.app.ruk-com.cloud", 
                                port="5432", 
                                database="pythonlogin")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM MoneyTHAPI ')
        money_records = cursor.fetchall()
        money_records = money_records[::-1]
        return render_template("tableTH.html", value=money_records) 
    return redirect(url_for('tableTH'))



@app.route('/pythonlogin/tablegoldTH')#ทองไทย
def tablegoldTH():
    if 'loggedin' in session:
        connection = psycopg2.connect(user="webadmin",
                                password="BFCqhr46914", 
                                host="node4943-env-2254395.th.app.ruk-com.cloud", 
                                port="5432", 
                                database="pythonlogin")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM GoldTH ')
        goldTH_records = cursor.fetchall()
        goldTH_records = goldTH_records[::-1]
        return render_template("tablegoldth.html", value=goldTH_records) 
    return redirect(url_for('tablegoldTH'))



@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))



@app.route('/pythonlogin/forgot', methods=['GET', 'POST'])
def forgot():
    msg = ''
    recode = ""
    if request.method == 'POST' and 'username' in request.form and 'new_password' in request.form  and 'code_repassword' in request.form and 'confirm_password' in request.form:
        username = request.form['username']
        newpassword = request.form['new_password']
        confirm_password = request.form['confirm_password']
        code_repassword = request.form['code_repassword']
        connection = psycopg2.connect(user="webadmin",
                                password="BFCqhr46914", 
                                host="node4943-env-2254395.th.app.ruk-com.cloud", 
                                port="5432", 
                                database="pythonlogin")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND code_repassword = %s', (username,code_repassword))
        account = cursor.fetchall()
        if account:
            if newpassword != confirm_password:
                msg = 'Please Enter Confirm Password like New Password.'
            elif not username or not newpassword or not confirm_password:
                msg = 'Please fill out the form!'
            else:
                for i in range(6):
                    i = random.randint(0,9)
                    recode += str(i)
                postgresSQL_select_Query ="update accounts set password = %s  where username =%s"
                cursor.execute(postgresSQL_select_Query,(newpassword,username))
                postgresSQL_select_Query ="update accounts set code_repassword =%s where username =%s"
                cursor.execute(postgresSQL_select_Query,(recode,username))
                connection.commit()
                msg2 = 'Please take note is '+recode+' for Repassword'
                msg = ['Change password successfully',msg2]
        else:
            msg = 'Incorrect username/code repassword!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('forgot.html', msg=msg)

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    recode =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'confirm_password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        connection = psycopg2.connect(user="webadmin",
                                password="BFCqhr46914", 
                                host="node4943-env-2254395.th.app.ruk-com.cloud", 
                                port="5432", 
                                database="pythonlogin")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif password != confirm_password:
            msg ='Please Enter Confirm Password like Password.'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            for i in range(6):
                i = random.randint(0,9)
                recode += str(i)
            code_repassword = recode
            postgres_insert_query = """ INSERT INTO accounts (username, password, email,code_repassword) VALUES (%s,%s,%s,%s)"""
            cursor.execute(postgres_insert_query,(username,password,email,code_repassword))
            connection.commit()
            msg2 = 'Please take note is '+recode+" for Repassword"
            msg = ['User register successfully',msg2]
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/home', methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html', account=session)
    return redirect(url_for('login'))
 
@app.route('/pythonlogin/about') 
def about():
    if 'loggedin' in session:
        return render_template('about.html', account=session)
    return redirect(url_for('login'))


if __name__ == '__main__' :
    app.run(debug=True,host='0.0.0.0',port=80)

