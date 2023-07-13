import os
import threading
import random
import datetime
import time

from flask import Flask
from flask import (make_response, redirect, render_template,
                   request, url_for, session)
from flask_sqlalchemy import SQLAlchemy

from config import AdminForm
import config

# f'''{self.artist_song}|*|{self.geneticist}|*|{self.difficult}|*|{self.video}|*|{self.download_url}|*|{self.song_id}'''

# 定义全局变量
data = ''
log_key_update = []
password = config.SECRET_KEY

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'secret_key')


def update_secret_key():
    global log_key_update
    while 1:
        app.config['SECRET_KEY'] = (os.urandom(24))
        # 配置WTF的CSRF，Value可以是任意的字符串
        app.config['WTF_CSRF_SECRET_KEY'] = (os.urandom(24))
        log_key_update.append(f"{datetime.date.today()} {time.strftime('%H:%M:%S')}")
        if len(log_key_update) > 10:
            log_key_update = log_key_update[:10]
        time.sleep(3600)


update_key = threading.Thread(target=update_secret_key)
update_key.setDaemon = True
update_key.start()

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


def db_get_data(req_id):
    try:
        data = AdofaiModsData().query.filter_by(id=req_id).all()[0]
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



@app.route('/admin-login', methods=['POST','GET'])
def login():
    global password  # 声明全局变量'
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
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


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'GET':
        pwd_cookie = session.get('password')  # 获取密码cookie
        pwd = pwd_cookie if pwd_cookie else None  # 如果cookie不存在，初始化密码为空

        if pwd == password:  # 如果密码正确，则返回内容
            pass
        elif pwd is None:
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
        return render_template('admin.html')
    if request.method == 'POST':
        request_dict = dict(request.form)
        if request_dict.get('data_action_select') == 'c':
            # 创建新的数据行
            new_data = AdofaiModsData(
                data_name=request_dict['data_name'],
                data_author=request_dict['data_author'],
                data_download_num=request_dict['data_download_num'],
                data_download_url=request_dict['data_download_url'],
                data_description=request_dict['data_description'],
                data_latest_version=request_dict['data_latest_version'],
            )
            # 添加到数据库
            db.session.add(new_data)
            db.session.commit()
        if request_dict.get('data_action_select') == 'f':
            try:
                result = AdofaiModsData.query.filter(AdofaiModsData.id == request_dict['data_id']).first()
                # 将要修改的值赋给title
                result.data_name = request_dict['data_name']
                result.data_author = request_dict['data_author']
                result.data_download_num = request_dict['data_download_num']
                result.data_download_url = request_dict['data_download_url']
                result.data_description = request_dict['data_description']
                result.data_latest_version = request_dict['data_latest_version']
                db.session.commit()
            except AttributeError as error:
                return render_template('404.html', error='修改的序号不存在！'), 404  # 返回模板和状态码
        if request_dict.get('data_action_select') == 'd':
            try:
                result = AdofaiModsData.query.filter(AdofaiModsData.id == request_dict['data_id']).first()
                db.session.delete(result)
                db.session.commit()
            except Exception as error:
                return render_template('404.html', error=f'错误，{error}'), 404  # 返回模板和状态码

        return redirect(url_for('list'))


    return render_template('admin.html')


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html', error=e), 404  # 返回模板和状态码


if __name__ == '__main__':
    # app.run(debug=True, host='127.0.0.1', port=9807)
    app.run(host='127.0.0.1', port=random.randint(999, 65535))
