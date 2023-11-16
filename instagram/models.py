# Vai as classes / estrura do banco de dados
from instagram import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    profile_img = database.Column(database.Text, nullable=False)

class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.String, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    comments = database.relationship('CommetsPost', backref='post', lazy=True)
    likes = database.relationship('LikesPost', backref='post', lazy=True)

class CommetsPost(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    comment_text = database.Column(database.String, nullable=False)
    creation_date = database.Column(database.String, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False)

class LikesPost(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    creation_date = database.Column(database.String, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False)

class Follows(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    creation_date = database.Column(database.String, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    user_follow_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
