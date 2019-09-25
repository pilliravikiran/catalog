from flask import Flask,redirect,url_for,render_template
app = Flask(__name__)
@app.route('/admin1')
def index():
	return "<h1> Welcome to my saaho wrld</h1>"


@app.route('/hello/<int:a>/<username>')
def hello(a,username):
    return 'Hello, {},{}'.format(username,a)

@app.route('/<int:a>')
def hi(a):
	return "%d"%a


@app.route('/admin3')
def admin():
	return "admin"


@app.route('/home/<text>')
def login(text):
	if(text == 'admin'):
		return redirect(url_for('admin'))
	else:
		return redirect(url_for('hello',a=1,username=2))

@app.route('/login/<int:name>/<int:val>')
def log(name,val):
	return render_template('index.html',name=name,val=val)
if __name__ == '__main__':
	app.run(host="localhost",port=80,debug=True)
