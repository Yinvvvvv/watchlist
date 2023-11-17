from flask import Flask
from flask import url_for
app = Flask(__name__)
@app.route('/')
def hello():
    return '<h1>hello 曹浩群!I love you！</h1><img src="http://helloflask.com/totoro.gif">'
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='amber'))
    print(url_for('user_page', name='chq'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=2))
    return 'Test page'