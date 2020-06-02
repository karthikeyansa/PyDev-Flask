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
	commentliked = db.relationship('CommentLike',foreign_keys = 'CommentLike.user_id',backref = 'user',lazy = 'dynamic')
	polls = db.relationship('Polls',backref = 'owner',cascade = "all, delete-orphan")
	voter = db.relationship('Pollvote',foreign_keys = 'Pollvote.user_id',backref = 'user',cascade = "all, delete-orphan")

	def like_post(self,post):
		if not self.has_liked_post(post):
			like = PostLike(user_id = self.id ,post_id =post.id)
			db.session.add(like)
	
	def unlike_post(self,post):
		if self.has_liked_post(post):
			PostLike.query.filter_by(user_id = self.id,post_id = post.id).delete()
	
	def has_liked_post(self,post):
		return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0
	
	def like_comment(self,comment):
		if not self.has_liked_comment(comment):
			like = CommentLike(user_id = self.id,comment_id = comment.id)
			db.session.add(like)
	
	def unlike_comment(self,comment):
		if self.has_liked_comment(comment):
			CommentLike.query.filter_by(user_id = self.id,comment_id = comment.id).delete()

	def has_voted_poll(self, poll):
		return Pollvote.query.filter(Pollvote.user_id == self.id,Pollvote.poll_id == poll.id).count() > 0
	
	def has_liked_comment(self,comment):
		return CommentLike.query.filter(CommentLike.user_id == self.id, CommentLike.comment_id == comment.id).count() > 0

	

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

	def __str__(self):
		return f'{self.id} {self.title} {self.content} {self.author}'

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
	likes = db.relationship('CommentLike',backref = 'comment',lazy = 'dynamic')

	def __str__(self):
		return f'{self.id} {self.content}'
class CommentLike(db.Model):
	__tablename__ = 'commentlike'
	id = db.Column(db.Integer,primary_key = True)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	comment_id = db.Column(db.Integer,db.ForeignKey('comments.id'))

class Polls(db.Model):
    __tablename__ = 'polls'
    id = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.Text,nullable = False)
    choice1 = db.Column(db.String(50),nullable = False)
    choice2 = db.Column(db.String(50),nullable = False)
    selected = db.Column(db.String(50),default = None)
    choice1_total = db.Column(db.Integer,nullable = False,default = 0)
    choice2_total = db.Column(db.Integer,nullable = False,default = 0)
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __str__(self):
        return f'{self.id} {self.question} {self.choice1} {self.choice2}'

    def sum(self):
        return f'{self.choice1} {sum({self.choice1_total})} {self.choice2} {sum({self.choice2_total})}'

class Pollvote(db.Model):
    __tablename__ = 'pollvote'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    poll_id = db.Column(db.Integer,db.ForeignKey('polls.id'))