from flask import Blueprint

app = Blueprint('admin',__name__, url_prefix="/admin")

@app.route("/")
def admin():
    return "ここは管理者用画面ですよ．"

@app.route("/login")
def login():
    return "ここは管理者用のログインページです"
