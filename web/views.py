
from flask import Blueprint, render_template, request, \
    redirect,url_for

from back.models import Article

web = Blueprint('web',__name__)


# 网站首页
@web.route('/index/',methods=['GET'])
def index():
    articles = Article.query.limit(10).all()
    return render_template('web/index.html', articles=articles)

# 关于我
@web.route('/about/', methods=['GET'])
def about():
    return render_template('web/about.html')

# 我的日记
@web.route('/list/', methods=['GET'])
def list():
    return render_template('web/list.html')


# 内容页
@web.route('/info/<int:id>/')
def info(id):
    article = Article.query.get(id)
    return render_template('web/info.html', article=article)