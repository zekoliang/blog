from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 用户的类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)
    is_delete = db.Column(db.Boolean, default=0)
    # 用户名创建的时间
    create_time = db.Column(db.DateTime, default=datetime.now)

    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()

# 文章的分类表
class ArticleType(db.Model):
    #类型id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 类型名称
    t_name = db.Column(db.String(10), unique=True, nullable=False)
    # 与外键关联关系
    arts = db.relationship('Article', backref='tp')

    __tablename__ = 'art_type'

# 文章表
class Article(db.Model):
    # 文章id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 文章标题
    title = db.Column(db.String(30),  unique=True, nullable=False)
    # 文章简单的描述
    desc = db.Column(db.String(100), nullable=False)
    # 文章详情的内容介绍
    content = db.Column(db.Text, nullable=False)
    # 文章创建的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 外键,关联分类表(一对多)
    type = db.Column(db.Integer, db.ForeignKey('art_type.id'))

    def save_update(self):
        db.session.add(self)
        db.session.commit()


