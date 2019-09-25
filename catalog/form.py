from flask import *

app = Flask(__name__)


@app.route('/login',methods=['GET'])
def data():
	if(request.method == "POST"):
		passwd=request.form['pass']
		uname=request.form['uname']
		file = request.files['file']
		file.save(file.filename)  
		if uname=="vp" and passwd=="2116":
			return "Welcome %s" %file.filename 
	else:
		passwd=request.args.get['pass']
		uname=request.args.get['uname']
		if uname=="vp" and passwd=="2116":
			return "Welcome %s" %uname 

@app.route('/l')
def login():
	return render_template('login.html')
if(__name__ == '__main__'):
	app.run(host='localhost',port=80,debug=True)
