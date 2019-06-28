from flask_bootstrap import Bootstrap
from flask import Flask, request, render_template, url_for, session, escape, redirect
import bbs_system_functions as system
import sqlalchemy_connDB as connDB2
from sqlalchemy_connDB import query_one

app = Flask(__name__)
bootstrap = Bootstrap(app)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/', methods=['GET', 'POST'])
def home():
    ''' 要把模板home.html放到正确的templates目录下，templates和app.py在同级目录下 '''
    if 'username' in session:
        return render_template('home.html', username=escape(session['username']))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']

        # 1. 判断有没有用户
        flag = system.login(username, userpass)
        if flag == 0:
            return render_template('login.html', message='username not find', info='')
        elif flag == 1:
            return render_template('login.html', message='userpass error', info='')
        else:   # flag == 2
            # 登录成功则存入会话
            session['username'] = request.form['username']
            # return render_template('home.html', message='login success', username=username, info='')
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['userpass']
        flag = system.register(username, userpass)
        if flag:
            session['register_flag'] = 'True'
            # return render_template('login.html', message='register success!')
            return redirect(url_for('signin'))
        else:
            return render_template('register.html', message='register error!')

    return render_template('register.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/update_user/', methods=['GET', 'POST'])
def update_user():
    # *** js判断输入是否合法(没有做）
    # 检查session
    if 'username' in session:
        if request.method == 'POST':
            user = system.User()
            user.id = request.form['id']
            user.username = request.form['username']
            user.userpass = request.form['userpass']
            user.usertype = request.form['usertype']
            user.usermail = request.form['usermail']
            user.userhomepage = request.form['userhomepage']
            user.homepagename = request.form['homepagename']
            user.sex = request.form['sex']
            user.comefrom = request.form['comefrom']
            user.usersign = request.form['usersign']
            user.redate = request.form['redate']
            user.update()
            session.pop('username', None)
            session['username'] = request.form['username']
            # 判断session.username是不是admin，如果不是admin则返回login页面
            result = user.query_all_by_username()[0][4]
            print(result)
            if result != 'admin':
                return redirect(url_for('logout'))
            return 'post ok'
        # 根据session中的用户名查找其所有信息
        user = system.User()
        user.username = session['username']
        # id = user.query_all_by_username()[0][0]
        result = user.query_all_by_username()
        return render_template('user_detail.html', result=result)
    return redirect(url_for('home'))


@app.route('/query_board', methods=['GET', 'POST'])
def query_board():
    board = system.Board()
    if request.method == 'POST':
        return render_template('board.html')
    # get操作，先获取数据库中的board
    query_board_sql = 'select * from board;'
    result = board.query_board(query_board_sql)
    return render_template('board.html', result=result, len_result=len(result))


@app.route('/save_board', methods=['GET', 'POST'])
def save_board():
    board = system.Board()
    if request.method == 'POST':
        update_board_sql = ''
        # result = board.update_board(update_board)
        return request.args
    return request.args


@app.route('/query_board2', methods=['GET', 'POST'])
def query_board2():
    board = system.Board()
    if request.method == 'POST':
        return render_template('board2.html')
    # get操作，先获取数据库中的board
    query_board_sql = 'select * from board;'
    result = board.query_board(query_board_sql)
    return render_template('board2.html', result=result)


@app.route('/update_board_detail', methods=['GET', 'POST'])
def update_board_detail():
    if request.method == 'POST':
        board = system.Board()
        board.update_board()
        return render_template('board_detail.html')
    return render_template('board_detail.html')


@app.route('/one')
def hello_world():
    return render_template('test.html')


@app.route('/test/', methods=['GET', 'POST'], endpoint='test01')
def test():
    getData = request.args # 利用request对象获取GET请求数据
    print('获取的GET数据为：', getData) # 打印获取到的GET数据 ImmutableMultiDict([])
    postData = request.form # 利用request对象获取POST请求数据
    print('获取的POST数据为：', postData) # 打印获取到的POST请求 ImmutableMultiDict([('username', '456'), ('password', '789')])
    username = request.form.get('username')
    password = request.form.get('password')
    print(username,password) #456 789
    return '这是测试页面'


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)     # debug=True 调试模式：服务器会在代码修改后自动重新载入，并在发生错误时提供一个相当有用的调试器
