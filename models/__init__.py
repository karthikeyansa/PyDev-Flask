from app import db
from flask_login import UserMixin
from datetime import datetime,timedelta

class User(UserMixin,db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80),nullable = False,unique = True)
	password = db.Column(db.String(80),nullable = False)
	email = db.Column(db.String(120), nullable = False,unique = True)
	created = db.Column(db.DateTime, default=datetime.now)
	color = db.Column(db.String(120),nullable = False)
	posts = db.relationship('Posts',backref ='owner',cascade ="all, delete-orphan")
	liked = db.relationship('PostLike',foreign_keys = 'PostLike.user_id',backref = 'user',lazy = 'dynamic')
	def like_post(self,post):
		if not self.has_liked_post(post):
			like = PostLike(user_id = self.id ,post_id =post.id)
			db.session.add(like)
	def unlike_post(self,post):
		if self.has_liked_post(post):
			PostLike.query.filter_by(user_id = self.id,post_id = post.id).delete()
	def has_liked_post(self,post):
		return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

class Posts(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer,primary_key = True)
	title = db.Column(db.String(100),nullable = False,default = 'N/A')
	content = db.Column(db.Text,nullable = False,default = 'N/A')
	author = db.Column(db.String(10),nullable = False,default = 'N/A')
	created = db.Column(db.DateTime, default=datetime.now)
	owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	likes = db.relationship('PostLike',backref = 'post',lazy ='dynamic')
	comments = db.relationship('Comments',backref = 'post',lazy='dynamic',cascade ="all, delete-orphan")

class PostLike(db.Model):
	__tablename__ = 'postlike'
	id = db.Column(db.Integer,primary_key = True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

class Comments(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer,primary_key = True)
	content = db.Column(db.Text,nullable = False,default = 'N/A')
	author = db.Column(db.String(10),nullable = False,default = 'N/A')
	created = db.Column(db.DateTime, default=datetime.now)
	color = db.Column(db.String(120),nullable = False)
	post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
