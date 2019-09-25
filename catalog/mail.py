from flask import *  
from flask_mail import Mail,Message  
from random import randint
app = Flask(__name__)  
  

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 465  
app.config['MAIL_USERNAME'] = 'jvvprasad04@gmail.com'  
app.config['MAIL_PASSWORD'] = 'jvvprasad123'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
  
 
mail = Mail(app)  
#app.secret_key="vv"
otp = randint(000000,999999)

@app.route('/') 
def email():
	return render_template("email.html") 
@app.route('/email_send',methods=['POST'])
def otp2():
	if(request.method == "POST"):
		receipt = request.form['email']
		msg = Message('otp', sender = 'jvvprasad04@gmail.com', recipients=[receipt])
		msg.body = str(otp)
		mail.send(msg)
		return render_template('verify.html')
    	
   	     
    
@app.route('/email_verify',methods=['POST'])
def verify():
	if(request.method == "POST"):
		otp1 = request.form['otp']
		if(int(otp1) == otp):
			return render_template("success.html",success="verified")
		else:
			return render_template("success.html",success="not verified")

if __name__ == '__main__':  
    app.run(debug = True,port='80',host='localhost')  