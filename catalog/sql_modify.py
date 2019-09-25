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


@app.route('/')
@login_required
def showData():
	data = session.query(Register).all()
	return render_template('show.html',data = data)

@app.route('/add')
def addData():
	return render_template('add_data.html')


@app.route('/adding',methods=['POST'])
def add_data():
	newData = Register(name = request.form['name'],
					   email = request.form['email'],
					   des = request.form['des']
					  )
	session.add(newData)
	session.commit()
	flash("New data is added")
	return redirect(url_for('showData'))
	
@app.route('/editdata/<int:edit_id>',methods=['POST','GET'])
def edit_data(edit_id):
	edit = session.query(Register).filter_by(id=edit_id).one()
	if(request.method == 'POST'):
		edit.name = request.form['name']
		edit.email = request.form['email']
		edit.des = request.form['des']				  
		session.add(edit)
		session.commit()
		return redirect(url_for('showData'))
	else:
		return render_template('edit_data.html',register=edit)		

@app.route('/deletedata/<int:delete_id>',methods=['POST','GET'])
def delete_data(delete_id):
	delete = session.query(Register).filter_by(id=delete_id).one()		  
	session.delete(delete)
	session.commit()
	return redirect(url_for('showData'))	

@app.route('/register',methods=['POST','GET'])
def registerData():
	regdata = User(name=request.form['name'],
					email=request.form['email'],
					password=request.form['passwd']
				)
	session.add(regdata)
	session.commit()
	return redirect(url_for('login'))
@app.route('/reg')
def register():
	return render_template('login_user.html')

@app.route('/login',methods=['POST',"GET"])
def login():
	if(current_user.is_authenticated):
		return redirect(url_for('showData'))
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
	return redirect(url_for('login'))
	
if(__name__ == '__main__'):
	app.run(debug=True,host="localhost",port=3000)