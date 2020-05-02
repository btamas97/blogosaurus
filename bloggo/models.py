from . import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', cascade="all, delete-orphan", backref='post', lazy=True)

    def __repr__(self):
        return '<Article {}>'.format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

