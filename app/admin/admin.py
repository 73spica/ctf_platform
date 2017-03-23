from flask import Blueprint
from flask import Flask, request, render_template, redirect,session, url_for, flash

app = Blueprint('admin',__name__, url_prefix="/admin",template_folder='../admin/templates')

@app.route("/")
def admin():
    return render_template("home_for_admin.html")

@app.route("/login")
def login():
    return render_template("login_for_admin.html")

@app.route("/problem")
def problem():
    return render_template("problem_for_admin.html")

