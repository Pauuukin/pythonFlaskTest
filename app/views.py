from datetime import datetime
from flask import render_template, flash, redirect, session,url_for, request, g
from flask_login import login_user, logout_user,current_user,login_required
from app import app, db
from app.__init__ import oid
from app.models import  User, ROLE_ADMIN, ROLE_USER
from app.forms import LoginForm, EditForm

@app.route('/index', endpoint = 'index')       #декораторы route создают привязку адресов к этой функции
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname' : 'User1'},
            'body': 'Some text! '
        },
        {
            'author': {'nickname': 'User2'},
            'body': 'another some text! '
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


#Чтобы отобразить пользовательские записи
#мы используем список, где у каждого элемента будут поля автор и основная часть.


#функция render_template вызывает шаблонизатор Jinja2,
#который является частью фреймворка Flask. Jinja2 заменяет блоки {{...}}
# на соответствующие им значения, переданные как аргументы шаблона.


@app.route('/login',methods=['GET','POST'], endpoint='login')
@oid.loginhandler               #Благодаря oid.loginhandler Flask-OpenID теперь знает, что это — функция для авторизации.
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me']= form.remember_me.data       # сохраняем значение поля remember_me в сессии Flask
        return oid.try_login(form.openid.data, ask_for= ['nickname','email'])   #запускает процесс авторизации с помощью Flask-OpenID.
                                                                                # Эта функция принимает два аргумента: openid, полученный из веб-формы
                                                                                # и список полей, которые мы хотели бы получить от провайдера OpenID
    return render_template('login.html',
                           title='Sign In',
                           form = form,
                           providers = app.config["OPENID_PROVIDERS"])


#g — это глобальный объект Flask, предназначенный для хранения и обмена данными
# во время жизни запроса. Именно в нём мы будем хранить данные о текущем пользователе.
# В верхней части тела функции мы проверяем значение g.user. Если пользователь уже авторизован,
# мы перенаправляем его на главную страницу.

# Функция url_for, которую мы использовали при вызове redirect,
# предоставляет возможность получения URL для переданного ей имени функции представления.

# Данные, сохраненные в сессии, будут также доступны во время всех последующих
# запросов от одного клиента. Информация хранится до тех пор, пока не будет явно удалена.
# Такое поведение возможно благодаря тому, что Flask хранит отдельные сессии для каждого клиента.


@oid.after_login
def after_login(resp):                          #Аргумент resp, переданный функции after_login содержит в себе данные, полученные от провайдера OpenID.
    if resp.email is None or resp.email =="":
        flash('Invalid login. Please try again. ')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

# В первую очередь нам необходимо проверить, что в ответе от сервера содержится
# email пользователя, в противном случае мы не можем его авторизовать.
# Проверяем, содержится ли полученный email в нашей базе данных. Если ничего не найдено,
# добавляем нового пользователя в базу. Стоит отметить, что некоторые провайдеры OpenID
# не предоставляют nickname, но для нас это не является проблемой, мы можем использовать имя из почты.

# После этого мы пытаемся получить значение remember_me из сессии Flask,
# это то самое значение, которое мы сохранили в функции представления login.

# Затем мы вызываем функцию login_user из модуля Flask-Login,
# чтобы наконец авторизовать пользователя в нашем приложении.

#В конце концов мы перенаправляем пользователя по адресу, переданному в атрибуте next,
# или же на главную страницу, если такой параметр в запросе отсутствует (см. txt)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


#Все функции, объявленные с помощью декоратора before_request будут запущены
# непосредственно перед вызовом функции отображения каждый раз, когда получен запрос.


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()    #грузим пользователя из базы данных, используя nickname который мы приняли в качестве аргумента.
    if user == None:
        flash('User ' +nickname + ' not found.')
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post 1'},
        {'author': user, 'body': 'Test post 2'}
    ]
    return render_template('user.html',
                           user = user,
                           posts = posts)

#Метод имеет параметр с именем nickname. Так же нужно добавить параметр во вью-функцию
# с тем же именем. Когда клиент запрашивает URL /user/miguel , функция
# в представлении должна вызываться с параметром nickname = 'miguel'.

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('edit.html',
                               form=form)