# coding:utf-8
from flask import Flask, request, render_template, redirect,session, url_for, flash
from flask import Blueprint
from peewee import *
from datetime import date
import json
import hashlib
from .model.model import Users, db_for_admin, Problems, db

# TODO: 全ての処理について，adminであるかのチェック処理を実装
# TODO: ログインしていない場合はhomeとloginページ以外すべてloginにリダイレクトさせる
# デバッグしにくいのでとりあえず後回しで良い

app = Blueprint('admin',__name__, url_prefix="/admin",template_folder='../admin/templates')

@app.route("/")
@app.route("/home")
def home():
    if not checkAdminLogin():
        return redirect(url_for('admin.login'))
    return render_template("home_for_admin.html")

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        user,msg = doLogin(request.form['username'],request.form['password'])
        if user:
            session['username'] = user.username
            session['logged_in'] = True
            session['is_admin'] = user.is_admin
            return redirect(url_for('admin.home'))
        else:
            error = msg
        return render_template('login_for_admin.html',error=error)
    else:
        return render_template('login_for_admin.html')

@app.route('/logout',methods=['GET'])
def logout():
    doLogout()
    return redirect(url_for('admin.login'))

@app.route("/problem")
def problem():
    if not checkAdminLogin():
        return redirect(url_for('admin.login'))
    problems = Problems.select()
    return render_template("problem_for_admin.html", problems=problems)

@app.route("/adding_problems",methods=['GET','POST'])
def adding_problems():
    if not checkAdminLogin():
        return redirect(url_for('admin.login'))
    if request.method=='POST':
        form_list = ['title','point','genre','flag','detail','author']
        for key in form_list:
            if not request.form[key]:
                message = "Please fill in all forms."
                return render_template('adding_problems.html',error=message)
        success = addProblem(request.form['title'], request.form['point'], request.form['genre'], request.form['flag'], request.form['detail'], request.form['author'])
        if success:
            message = "Successfully added the problem."
            return render_template('adding_problems.html',success=message)
        else:
            error = "Failed to add problem. Please again."
            return render_template('adding_problems.html',error=message)
    else:
        return render_template("adding_problems.html")

def addProblem(title, point, genre, flag, detail, author):
    try:
        with db.transaction():
            # フラグもハッシュ取る
            flag = hashlib.md5(flag.encode("utf-8")).hexdigest()
            problem = Problems(name=title, point=point, genre=genre, flag=flag, author=author, detail=detail)
            problem.save()
        return True
    except IntegrityError as ex:
        print (ex)
        db.rollback()
        return False

# TODO: 問題の詳細画面が必要
# これはユーザと共通のUIで良いが，編集ボタンや削除ボタンを持つ．
# ユーザ用作ったのでそれのルーティングとhtmlをコピペする
@app.route('/problem/<int:p_id>',methods=['GET','POST'])
def problem_detail_for_admin(p_id):
    if not checkAdminLogin():
        return redirect(url_for('admin.login'))
    problem = Problems.get(Problems.id == p_id)
    if request.method=='POST':
        if not checkAdminLogin():
            return redirect(url_for('admin.login'))
        correct = checkFlag(p_id,request.form['input_flag'])
        return render_template('problem_detail_for_admin.html',problem=problem,correct=correct)
    else:
        return render_template('problem_detail_for_admin.html',problem=problem)

@app.route('/problem/edit/<int:p_id>',methods=['GET','POST'])
def editting_problem(p_id):
    if not checkAdminLogin():
        return redirect(url_for('admin.login'))
    problem = Problems.get(Problems.id == p_id)
    if request.method=='POST':
        if problem.name != request.form['title']:
            problem.name = request.form['title']
        if problem.point != request.form['point']:
            problem.point = request.form['point']
        if problem.genre != request.form['genre']:
            problem.genre = request.form['genre']
        if problem.detail != request.form['detail']:
            problem.detail = request.form['detail']
        if problem.author != request.form['author']:
            problem.author = request.form['author']
        if request.form['flag']:
            flag = request.form['flag']
            flag = hashlib.md5(flag.encode("utf-8")).hexdigest()
            problem.flag = flag
        problem.save()
        success = True
        return render_template('editing_problem.html', problem=problem, success=success)
    else:
        return render_template('editing_problem.html', problem=problem)

# TODO: 問題の編集画面が必要．
# adminのみの画面．一度登録した問題の編集が可能．

# TODO: 問題の削除処理が必要
# 問題IDとか作るか微妙だけど問題名がかぶることはまずないのでそれをユニークにしてしまってよい気がする．

def doLogin(username,password):
    try:
        with db_for_admin.transaction():
            pass_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
            user = Users.get(Users.username==username and Users.password==pass_hash)
    except (IntegrityError,Users.DoesNotExist) as ex:
        print (ex)
        db_for_admin.rollback()
        message = "username/password is wrong."
        return (False,message)
    else:
        if user:
            message = "Login Success!"
            return (user,message)
        else:
            message = "username/password is wrong."
            return (False,message)

@app.route('/register',methods=['POST'])
def register():
    if not checkAdminLogin():
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        # TODO: Registerページとログインページを分ける
        # 現状だとloginページにいるのにアドレスがregisterになる
        if doRegister(request.form['username'],request.form['password']):
            return render_template('login_for_admin.html',success=True)
        else:
            error = "Register failed."
            return render_template('login_for_admin.html',error=error)

def doRegister(username,password):
    try:
        with db_for_admin.transaction():
            pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
            user = Users(username=username, password=pass_hash, created_at=date.today(), is_admin=True, is_active=True, score=0, solved=json.dumps([]))
            user.save()
        return True
    except IntegrityError as ex:
        print (ex)
        db_for_admin.rollback()
        return False

# TODO: セッションに入れるキーはどこかにまとめておくべき？
def doLogout():
    session.pop('logged_in', None)
    session.pop('is_admin', None)

def checkAdminLogin():
    if "logged_in" in session:
        if not session['logged_in']:
            return False
    else:
        return False

    if "is_admin" in session:
        if not session['is_admin']:
            return False
    else:
        return False

    return True
def checkFlag(p_id,input_flag):
    input_flag = hashlib.md5(input_flag.encode('utf-8')).hexdigest()
    problem = Problems.get(Problems.id == p_id)
    correct_flag = problem.flag
    print(correct_flag)
    return input_flag == correct_flag
