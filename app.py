import os
import sys
import click

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

#创建Flask应用实例
app = Flask(__name__)

#创建数据库连接的URI，即数据库的位置
# 修改下面的配置为你的 MySQL 数据库信息
db_user = 'root'
db_password = '123456'
db_host = 'localhost'
db_name = 'moviedb'

# 使用 MySQL 数据库连接 URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
app.config['SQLALCHEMY_DATABASE_CHARSET'] = 'utf8'  # 使用 utf8mb4 字符集

db=SQLAlchemy(app)

#定义数据模型
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True) #主键
    name=db.Column(db.String(20)) #名字

class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True) #主键
    title=db.Column(db.String(60)) #电影标题
    year=db.Column(db.String(4)) #电影年份

#自定义命令initdb,创建数据库
@app.cli.command() #注册为命令
@click.option('--drop', is_flag=True, help='Create after drop')
    #设置选项
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') 

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Amber'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)
