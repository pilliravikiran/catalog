from flask import *  
from db import Register,Base,User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager,current_user,login_user,logout_user,login_required

app = Flask(__name__)
app.secret_key="ee"

Login_manager = LoginManager(app)
Login_manager.login_view = 'login'
Login_manager.login_message_category = 'info'

@Login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))

engine = create_engine('sqlite:///register.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()


@app.route('/Index')
def showData():
	data = session.query(Register).all()
	return render_template('Project_Index.html',data = data)
@app.route('/register')
def register():
	return render_template('reg_user.html')
@app.route('/registerData',methods=['POST','GET'])
def registerData():
	regdata = User(name=request.form['name'],
					email=request.form['email'],
					password=request.form['passwd']
				)
	session.add(regdata)
	session.commit()
	return redirect(url_for('login'))

@app.route('/login',methods=['POST',"GET"])
def login():
	if(current_user.is_authenticated):
		return redirect(url_for('login'))
	try:
		if(request.method == "POST"):
			user = session.query(User).filter_by(
					email=request.form['email'],
					password=request.form['passwd']
				).first()
			if user:
				login_user(user)
				return redirect(url_for("showData"))
			else:
				flash ('login failed')
		else:
			return render_template('Index_user.html')
	except Exception as e:
		flash("login failed")
	else:
		return render_template('Index_user.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('showData'))
	
	
if(__name__ == '__main__'):
	app.run(debug=True,host="localhost",port=3000)