import os
import ast
import platform

from flask import (Flask, Response, make_response, redirect, render_template,
                   request, url_for, session, jsonify)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

import threading

# f'''{self.artist_song}|*|{self.geneticist}|*|{self.difficult}|*|{self.video}|*|{self.download_url}|*|{self.song_id}'''

# 定义全局变量
data = ''
password = config.SECRET_KEY

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'secret_key')

app.config['SECRET_KEY'] = (os.urandom(24))

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 绑定Flask对象
db = SQLAlchemy(app)


class AdofaiModsData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_name = db.Column(db.String(512))
    data_author = db.Column(db.String(512))
    data_download_num = db.Column(db.String(512))
    data_download_url = db.Column(db.String(512))
    data_description = db.Column(db.String(512))
    data_latest_version = db.Column(db.String(512))

    def __repr__(self):
        return f'{self.data_name}|*|{self.data_author}|*|{self.data_download_num}|*|{self.data_description}|*|{self.data_latest_version}|*|{self.data_download_url}|*|{self.id}'


def db_get_data(id):
    try:
        data = AdofaiModsData().query.filter_by(id=id).all()[0]
    except Exception as error:
        return False
    return str(data)


def db_get_all_data():
    users = AdofaiModsData().query.all()
    data = []
    for i in range(len(users)):
        data.append(str(users[i]))
    return data


with app.app_context():
    db.create_all()


class MyForm(FlaskForm):
    name = StringField('模组名称/Name:')
    author = StringField('作者/Author:')
    download_num = StringField('下载/DownloadNumber:')
    description = StringField('简介/Description:')
    download_url = StringField('下载链接/DownloadURL:')
    l_version = StringField('最新版本/LatestVersion:')
    submit = SubmitField('提交/Submit')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def list():
    try:
        idata = db_get_all_data()
        if not idata:
            error = "No Data Has Found"
            return render_template('404.html', error=error), 404  # 返回模板和状态码
        final_data = []
        for i in range(len(idata)):
            final_data.append(idata[i].strip().split('|*|'))

    except Exception as error:
        return render_template('404.html', error=error), 404  # 返回模板和状态码
    return render_template('list.html', data=final_data)


@app.route('/admin-login')
def login_static():
    return render_template('login.html')


@app.route('/admin-login', methods=['POST'])
def login_post():
    global password  # 声明全局变量'
    form = MyForm()
    pwd = request.form['password']  # 获取用户提交的密码

    if pwd == password:  # 判断密码是否正确
        resp = make_response('<meta http-equiv="Refresh" content="0;url=../admin" />')  # 使用表单渲染模板
        session['password'] = pwd  # 将密码存储在cookie中
        return resp
    else:
        return render_template('login.html', error='密码错误')


@app.route('/mod/<int:mod_id>')
def get_song(mod_id):
    result = db_get_data(mod_id)
    if not result:
        pass
    elif str(result):
        return render_template('info.html', item=result.strip().split('|*|'))
    else:
        pass
    return render_template('404.html', error='Song Not Found'), 404  # 返回模板和状态码


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    pwd_cookie = session.get('password')  # 获取密码cookie
    pwd = pwd_cookie if pwd_cookie else ''  # 如果cookie不存在，初始化密码为空

    form = MyForm()

    if pwd == password:  # 如果密码正确，则返回内容
        pass
    elif pwd == '':
        return '''
<script>
function myFunction()
{alert("未登录！");}
myFunction()
</script>
<meta http-equiv="Refresh" content="0;url=../admin-login" />
'''  # 否则重定向至登录页面
    else:
        return '''
<script>
function myFunction()
{alert("密码错误！");}
myFunction()
</script>
<meta http-equiv="Refresh" content="0;url=../admin-login" />
'''  # 否则重定向至登录页面

    if form.validate_on_submit():
        if form.name.data and form.download_num.data and form.description.data and form.download_url.data and form.author.data:
            # 创建新的数据行
            new_data = AdofaiModsData(
                data_name=form.name.data,
                data_author=form.author.data,
                data_download_num=form.download_num.data,
                data_download_url=form.download_url.data,
                data_description=form.description.data,
                data_latest_version=form.l_version.data,
            )
            # 添加到数据库
            db.session.add(new_data)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return '''
<script>
function myFunction()
{alert("不能提交空值！");}
myFunction()
</script>
<meta http-equiv="Refresh" content="0" />
'''
    return render_template('admin.html', form=form)


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', error=e), 404  # 返回模板和状态码


if __name__ == '__main__':
    # app.run(debug=True, host='127.0.0.1', port=9807)
    app.run(host='127.0.0.1', port=9801)
