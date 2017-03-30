# coding:utf-8
from flask import Flask, request, render_template, redirect,session, url_for, flash
from peewee import *
from model.model import Problems, Users, db
from datetime import date
import json
import hashlib
from admin import admin

app = Flask(__name__)
app.register_blueprint(admin.app)

# ルーティング
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/problem')
def problem():
    problems = Problems.select()
    return render_template('problem.html', problems=problems)

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        #if valid_login(request.form['username'],request.form['password']):
        success,msg = doLogin(request.form['username'],request.form['password'])
        if success:
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = msg
        return render_template('login.html',error=error)
    else:
        return render_template('login.html')

@app.route('/logout',methods=['GET'])
def logout():
    doLogout()
    return redirect(url_for('login'))

@app.route('/register',methods=['POST'])
def register():
    print(request.form['password'])
    if request.method == 'POST':
        if doRegister(request.form['username'],request.form['password']):
            return render_template('login.html',success=True)
        else:
            error = "Register failed."
            return render_template('login.html',error=error)

#@app.route('/upload',methods=['GET','POST'])
#def upload_file():
#    if request.method == 'POST':
#        f = request.files['the_file']
#        f.save('./upfiles/uploaded_file.txt')
#        return 'アップロードが完了しました'
#    else:
#        return render_template('upload.html')


def doLogin(username,password):
    try:
        with db.transaction():
            pass_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
            user = Users.get(Users.username==username and Users.password==pass_hash)
    except (IntegrityError,Users.DoesNotExist) as ex:
        print (ex)
        db.rollback()
        message = "username/password is wrong."
        return (False,message)
    else:
        if user:
            message = "Login Success!"
            return (True,message)
        else:
            message = "username/password is wrong."
            return (False,message)

def doLogout():
    session.pop('logged_in', None)
    session.pop('is_admin', None)

def doRegister(username,password):
    try:
        with db.transaction():
            pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
            user = Users(username=username, password=pass_hash, created_at=date.today(), is_active=True, score=0, solved=json.dumps([]))
            user.save()
        return True
    except IntegrityError as ex:
        print (ex)
        db.rollback()
        return False

app.secret_key = '\xdc{\xb6\xaa\xa4=j\xd6\xfe\xcf\x9f\x11\x87T%R\xd9\xc1\x0f\xce\x08\x93O\xbc'
