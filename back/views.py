import math

from flask import Blueprint, render_template, request, \
    redirect, url_for, session

# 导入编码和解码
from werkzeug.security import generate_password_hash,\
    check_password_hash

from back.models import User, Article, ArticleType, db
from utils.functiond import is_login, get_page

back = Blueprint('back',__name__)


@back.route('/creat/', methods=['GET'])
def creat():
    db.create_all()
    return '创建表成功'


# 注册
@back.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 校验
        if username and password and password2:
            # 先判断该账号是否被注册过
            user = User.query.filter(User.username == username).first()
            if user:
                # 判断该账号已被注册过
                error = '该账号已被注册,请更换账号'
                return render_template('back/register.html', error=error)
            else:
                # 校验密码
                if password2 == password:
                    #保存数据
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    #跳转到登录界面
                    return redirect(url_for('back.login'))
                else:
                    # 密码错误
                    error = '两次密码不一致'
                    return render_template('back/register.html', error=error)
        else:
            error = '请填写完整的信息'
            return render_template('back/register.html', error=error)

# 登录
@back.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')

    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        # 校验用户名和密码是否存在
        if username and password:
            user = User.query.filter(User.username == username).first()
            # 校验用户名
            if not user:
                error = '该账号不存在,请先去注册'
                return render_template('back/login.html', error=error)
            # 校验密码
            if not check_password_hash(user.password,password):
                error = '密码错误,请修改密码'
                return render_template('back/login.html', error=error)
            # 账号和密码匹配,跳转到首页
            session['user_id'] = user.id
            return redirect(url_for('back.index'))

        else:
            error = '请填写完整的登录信息'
            return render_template('back/login.html', error=error)

# 注销/退出登录
@back.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


# 报告首页
@back.route('/index/', methods=['GET'])
@is_login
def index():
    users = User.query.filter(User.id == session['user_id']).first()
    user = len(User.query.all())
    articles = Article.query.all()
    counts_article = len(articles)
    return render_template('back/index.html', users=users, user=user, counts_article=counts_article)


# 文章分类
@back.route('/a_type/', methods=['GET', 'POST'])
def a_type():
    if request.method == 'GET':
        # 取出所有标题值
        types = ArticleType.query.all()
        counts_types=len(types)
        users = User.query.filter(User.id == session['user_id']).first()
        return render_template('back/article.html',users=users,types=types, counts_types=counts_types)


# 添加文章分类
@back.route('/add_type/', methods=['GET', 'POST'])
def add_type():
    if request.method == 'GET':
        users = User.query.filter(User.id == session['user_id']).first()
        return render_template('back/add_category.html', users=users)
    if request.method == 'POST':
        users = User.query.filter(User.id == session['user_id']).first()
        atype = request.form.get('atype')
        if atype:
            type1 = ArticleType.query.filter(ArticleType.t_name == atype).first()
            if not type1:
                # 保存文章分类信息
                art_type = ArticleType()
                art_type.t_name = atype
                db.session.add(art_type)
                db.session.commit()
                return redirect(url_for('back.a_type'))
            else:
                error = '文章类名重复'
                return render_template('back/add_category.html', error=error, users=users)
        else:
            error = '请填写文章类名'
            return render_template('back/add_category.html', error=error, users=users)

# 删除文章分类
@back.route('/del_type/<int:id>/', methods=['GET'])
def del_type(id):
    # 删除文章分类
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


# 文章列表
@back.route('/article_list/', methods=['GET', 'POST'])
def article_list():
    articles = Article.query.all()
    counts_article = len(articles)
    users = User.query.filter(User.id == session['user_id']).first()
    return render_template('back/article_list.html', articles=articles, users=users, counts_article=counts_article)


# 添加文章页面
@back.route('/article_add/', methods=['GET', 'POST'])
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        users = User.query.filter(User.id == session['user_id']).first()
        return render_template('back/article_detail.html', types=types, users=users)
    if request.method == 'POST':
        types = ArticleType.query.all()
        users = User.query.filter(User.id == session['user_id']).first()
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            title2 = Article.query.filter(Article.title == title).first()
            if not title2:
                #保存文章
                art = Article()
                art.title = title
                art.desc = desc
                art.content = content
                art.type = category
                db.session.add(art)
                db.session.commit()
                return redirect(url_for('back.article_list'))
            else:
                error = '文章标题重复'
                return render_template('back/article_detail.html', error=error,types=types, users=users)
        else:
            error = '请填写完整的文章信息'
            return render_template('back/article_detail.html', error=error, types=types, users=users)

# 删除文章列表
@back.route('/del_list/<int:id>/', methods=['GET'])
def del_list(id):
    # 删除文章列表
    alist = Article.query.get(id)
    db.session.delete(alist)
    db.session.commit()
    return redirect(url_for('back.article_list'))


# 修改文章列表
@back.route('/update_article/<int:id>/', methods=['GET','POST'])
def update_article(id):
    if request.method == 'GET':
        lists = Article.query.get(id)
        lists2 = ArticleType.query.all()
        users = User.query.filter(User.id == session['user_id']).first()
        return render_template('back/update_article.html', lists=lists, lists2=lists2, users=users)
    if request.method == 'POST':
        users = User.query.filter(User.id == session['user_id']).first()
        title = request.form.get('title')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        create_time = request.form.get('time')
        # 保存更新的文章
        art = Article.query.get(id)
        art.title = title
        art.desc = desc
        art.content = content
        art.type = category
        art.create_time = create_time
        db.session.commit()
        return redirect(url_for('back.article_list'))
