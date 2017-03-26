# coding:utf-8
from flask import Flask, request, render_template, redirect,session, url_for, flash
from flask import Blueprint
from peewee import *
from datetime import date
import json
import hashlib
from model.model import Users, db

app = Blueprint('admin',__name__, url_prefix="/admin",template_folder='../admin/templates')

@app.route("/")
@app.route("/home")
def home():
    return render_template("home_for_admin.html")

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        #if valid_login(request.form['username'],request.form['password']):
        success,msg = doLogin(request.form['username'],request.form['password'])
        if success:
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('admin.home'))
        else:
            error = msg
        return render_template('login_for_admin.html',error=error)
    else:
        return render_template('login_for_admin.html')

@app.route('/logout',methods=['GET'])

@app.route("/problem")
def problem():
    return render_template("problem_for_admin.html")


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

@app.route('/register',methods=['POST'])
def register():
    print(request.form['password'])
    if request.method == 'POST':
        if doRegister(request.form['username'],request.form['password']):
            return render_template('login_for_admin.html',success=True)
        else:
            error = "Register failed."
            return render_template('login_for_admin.html',error=error)

def doRegister(username,password):
    try:
        with db.transaction():
            pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
            user = Users(username=username, password=pass_hash, created_at=date.today(), is_admin=True, is_active=True, score=0, solved=json.dumps([]))
            user.save()
        return True
    except IntegrityError as ex:
        print (ex)
        db.rollback()
        return False

