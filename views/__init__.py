from app import app,db
from datetime import datetime,timedelta
from flask import render_template,session,redirect,url_for,request,jsonify,flash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from models import User,Posts,PostLike,Comments
import re,requests,smtplib,random


loginmanager = LoginManager()
loginmanager.init_app(app)

@loginmanager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/',methods = ['GET','POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username = username,password = password).first()
		if user:
			login_user(user)
			cur_user = current_user.username
			session['user_val'] = '%s'%(cur_user,)
			return redirect('/home/%s'%(cur_user,))
		else:
			msg = 'Invalid User'
			return render_template('index.html',msg = msg)
	return render_template('index.html')

@app.route('/account')
@login_required
def account():
	user_val = session.get('user_val', None)
	user = User.query.filter_by(username = user_val).first()
	username = user.username
	email = user.email
	created = user.created
	color = user.color
	posts = len(user.posts)
	return render_template('account.html',username = username,created = created,email = email,posts = posts,color = color)
#olduser
def finaluser(email,subject,msg):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login("impowaste39@gmail.com","Letsfuck39")
		message = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail("impowaste39@gmail.com",email, message)
		server.quit()
		return "account deleted successfully"
	except:
		return "The email account that you tried to reach does not exists.Please try double-checking the recipient's email address for typos or unnecessary spaces."

@app.route('/account/delete')
@login_required
def delete_account():
	user_val = session.get('user_val', None)
	user = User.query.filter_by(username = user_val).first()
	email = user.email
	db.session.delete(User.query.get(user.id))
	db.session.commit()
	subject = 'Goodbye from PyDev'
	message = 'Hello %s.\n\nThis email is to confirm PyDev has DELETED all your user-data from its servers.\n\nThankyou for being a member of PyDev community.\n\nWishing you all the best,%s\nPyDev'%(user_val,user_val)
	finaluser(email,subject,message)
	flash('Your account "%s" has been deleted successfully'%(user_val))
	return redirect('/')
#newuser
def newuser(email,subject,msg):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login("impowaste39@gmail.com","Letsfuck39")
		message = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail("impowaste39@gmail.com",email, message)
		server.quit()
		return "We have send your password to your registered email account"
	except:
		return "The email account that you tried to reach does not exists.Please try double-checking the recipient's email address for typos or unnecessary spaces."

def randomcolor():
	lists = random.choices(['red','blue','green','orange','purple','yellow'])
	return ''.join(lists)

@app.route('/register',methods = ['GET','POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		color = randomcolor()
		created = datetime.now()+timedelta(hours = 5,minutes = 30)
		account = User.query.filter_by(username = username).all()
		accountemail = User.query.filter_by(email = email).all()
		if account:
			msg = 'Account already exists!'
			return jsonify({'message':msg})
		elif accountemail:
			msg = 'Email already registered!'
			return jsonify({'message':msg})
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address!'
			return jsonify({'message':msg})
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers!'
			return jsonify({'message':msg})
		elif not username or not password or not email:
			msg = 'Please fill out the form!'
			return jsonify({'message':msg})
		else:
			new_user = User(username = username,password = password,email = email,color=color,created = created)
			db.session.add(new_user)
			db.session.commit()
			email = new_user.email
			username = new_user.username
			password = new_user.password
			subject = 'Hello From PyDev'
			message = 'Hello %s.\n\nThankyou for registering at PyDev.Share us your developer stories,your ups and downs and help us to build a open source community.\n\nYour PyDev account username is "%s".\nYour PyDev account password is "%s".\n\nRegards: PyDev'%(username,username,password,)
			newuser(email,subject,message)
			msg = 'You have successfully registered!'
			return render_template('index.html',msg2 = msg)
	elif request.method == 'POST':
		msg = 'Please fill the form'
		return jsonify({'message':msg})
	return render_template('register.html')

@app.route('/logout',methods = ['GET','POST'])
@login_required
def logout():
	cur_user = current_user.username
	logout_user()
	flash('You are logged out %s successfully'%(cur_user))
	return redirect('/')

@app.route('/posts',methods = ['GET','POST'])
@login_required
def posts():
	user_val = session.get('user_val', None)
	user = User.query.filter_by(username = user_val).first()
	color = user.color
	if request.method == 'POST':
		title = request.form['title']
		content =  request.form['content']
		author = user_val
		created = datetime.now()+timedelta(hours = 5,minutes = 30)
		user = User.query.filter_by(username = user_val).first()
		new_post = Posts(title = title,content = content,author = author,owner = user,created = created)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	else:
		allposts = Posts.query.order_by(Posts.created.desc()).all()
		return render_template('post.html',posts = allposts,id = id,color = color)

@app.route('/home/<cur_user>',methods = ['GET','POST'])
@login_required
def home(cur_user):
	user_val = session.get('user_val', None)
	if request.method == 'POST':
		title = request.form['title']
		content =  request.form['content']
		author = user_val
		created = datetime.now()+timedelta(hours = 5,minutes = 30)
		user = User.query.filter_by(username = user_val).first()
		new_post = Posts(title = title,content = content,author = author,owner = user,created = created)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/home/%s'%(user_val,))
	else:
		some = User.query.filter_by(username = user_val).first()
		some.posts.reverse()
		allposts = some.posts
		#allposts = Posts.query.order_by(Posts.created.desc()).all()
		return render_template('home.html',posts = allposts,id = id,user = cur_user,color = some.color)

@app.route('/home/delete/<int:id>')
@login_required
def delete(id):
	user_val = session.get('user_val', None)
	post = Posts.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	flash('Post %d deleted successfully'%(id,))
	return redirect('/home/%s'%(user_val,))

@app.route('/home/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit(id):
	user_val = session.get('user_val', None)
	post = Posts.query.get_or_404(id)
	if request.method == 'POST':
		post.title = request.form['title']
		post.content = request.form['content']
		post.author = user_val
		db.session.commit()
		flash('Edited successfully Post:%d'%(id,))
		return redirect('/posts')
	else:
		return render_template('edit.html',post = post)

@app.route('/comment/<int:id>',methods = ['GET','POST'])
@login_required
def comment(id):
	user_val = session.get('user_val',None)
	user = User.query.filter_by(username = user_val).first()
	post = Posts.query.get_or_404(id)
	if request.method == 'POST':
		content = request.form['content']
		author = user_val
		color = user.color
		created = datetime.now()+timedelta(hours = 5,minutes = 30)
		comment = Comments(content = content,author = author,post = post,color = color,created = created)
		db.session.add(comment)
		db.session.commit()
		return redirect('/comments')
	else:
		return render_template('newcomment.html',post = post)

@app.route('/comments',methods = ['GET','POST'])
@login_required
def comments():
	user_val = session.get('user_val',None)
	allcomments = Comments.query.order_by(Comments.created.desc()).all()
	return render_template('comments.html',comments = allcomments,user = user_val)

@app.route('/comment/delete/<int:id>',methods = ['GET','POST'])
@login_required
def delete_comment(id):
    comment = Comments.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment %d deleted successfully'%(id,))
    return redirect('/comments')

@app.route('/posts/new',methods = ['GET','POST'])
@login_required
def newpost():
	user_val = session.get('user_val', None)
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		author = user_val
		created = datetime.now()+timedelta(hours = 5,minutes = 30)
		user = User.query.filter_by(username = user_val).first()
		new_post = Posts(title = title,content = content,author = author,owner = user,created = created)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('newpost.html',cur_val = user_val)

@app.route('/search')
@login_required
def search():
	query = request.args.get('title')
	if len(query) == 0:
		return redirect(request.referrer)
	else:
		resp = Posts.query.filter(Posts.title.ilike(f'%{query}%')).all()
		resp.reverse()
		return render_template('searchpost.html',posts = resp)

@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Posts.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/forgot')
def forgot():
	return render_template('forgot.html')

#mail recovery
def mail(email,subject,msg):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login("impowaste39@gmail.com","Letsfuck39")
		message = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail("impowaste39@gmail.com",email, message)
		server.quit()
		flash('We have send your password to your registered email account')
	except:
		flash('The email account that you tried to reach does not exists')

@app.route('/recover',methods = ['GET','POST'])
def recover():
	if request.method == 'POST':
		unknown = request.form['username']
		unknownuser = User.query.filter_by(username = unknown).first()
		unknownemail = User.query.filter_by(email = unknown).first()
		if unknownuser:
			username = unknownuser.username
			password = unknownuser.password
			email = unknownuser.email
			subject = 'Password Recovery From PyDev'
			message = 'Hello %s.\n\nYour PyDev account password is "%s".\n\nNOTE:If you have not requested password change, your account would have been hacked.Kindly mail us for any queries.\n\nMail ID: impowaste39@gmail.com\n\nRegards: PyDev'%(username,password,)
			msg = mail(email,subject,message)
			return redirect('/forgot')
		elif unknownemail:
			username = unknownemail.username
			password = unknownemail.password
			email = unknownemail.email
			subject = 'Password Recovery From PyDev'
			message = 'Hello %s.\n\nYour PyDev account password is "%s".\n\nNOTE:If you have not requested password change, your account would have been hacked.Kindly mail us for any queries.\n\nMail ID: impowaste39@gmail.com\n\nRegards: PyDev'%(username,password,)
			msg = mail(email,subject,message)
			return redirect('/forgot')
		else:
			flash('No search results found!')
			return redirect('/forgot')
#password change
def changemail(email,subject,msg):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login("impowaste39@gmail.com","Letsfuck39")
		message = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail("impowaste39@gmail.com",email, message)
		server.quit()
		flash('Password changed successfully')
	except:
		flash('The email account that you tried to reach does not exists')
@app.route('/changepassword',methods = ['GET','POST'])
@login_required
def changepassword():
	user_val = session.get('user_val', None)
	if request.method == 'POST':
		user = User.query.filter_by(username = user_val).first()
		newpassword = request.form['newpassword']
		retypepassword = request.form['retypepassword']
		oldpassword = user.password
		if newpassword == retypepassword and newpassword != oldpassword:
			user.password = newpassword
			db.session.commit()
			username = user.username
			password = user.password
			email = user.email
			subject = 'Password Changed From PyDev'
			message = 'Hello %s.\n\nYour PyDev account password is "%s".\n\nNOTE:If you have not requested password change, your account would have been hacked.Kindly mail us for any queries.\n\nMail ID: impowaste39@gmail.com\n\nRegards: PyDev'%(username,password,)
			msg = changemail(email,subject,message)
			return redirect('/account')
		else:
	 		flash('Password mismatch or typed current password')
	 		return redirect('/changepassword')
	else:
		user = User.query.filter_by(username = user_val).first()
		oldpassword = user.password
		return render_template('updatepassword.html',oldpassword = oldpassword)

@app.context_processor
def context_processor():
	user_val = session.get('user_val', None)
	return dict(key = user_val)

#########Extras##########
########weather#########
@app.route('/weather')
@login_required
def index():
    return render_template('weather_idx.html')

@app.route('/temperature', methods=['GET','POST'])
@login_required
def temperature():
	if request.method == 'POST':
		try:
		    zipcode = request.form['zip']
		    r = requests.get(
		        'https://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',in&appid=ba7bb2fcd4d0e41b8155727a76289e9f')
		    jsonobj = r.json()
		    temp_k = float(jsonobj['main']['temp'])
		    temp_c = temp_k - 273.15
		    temp_c = round(temp_c)
		    return render_template('temperature.html', temp=temp_c, zipcode=zipcode)
		except:
		 	message = 'Enter a valid PIN code'
		 	return jsonify({'message':message})
	else:
		flash('Enter a valid PIN code')
		return redirect('/weather')