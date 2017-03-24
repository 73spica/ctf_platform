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
def admin():
    return render_template("home_for_admin.html")

@app.route("/login")
def login():
    return render_template("login_for_admin.html")

@app.route("/problem")
def problem():
    return render_template("problem_for_admin.html")

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

