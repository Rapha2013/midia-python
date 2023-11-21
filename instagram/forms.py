# Aqui vai ficar os formularios de login e de posts

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.widgets import TextArea

from instagram.models import User

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    btn = SubmitField('Entrar')


class FormCreateNewAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Nome Completo', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    checkPassword = PasswordField('Confirmar Senha', validators=[DataRequired(), Length(6, 20), EqualTo('password')])
    profile_img = FileField('Imagem de Perfil', validators=[DataRequired()])
    btn = SubmitField('Criar Conta')

    def validate_email(self, email):
        email_of_user = User.query.filter_by(email=email.data).first()
        if email_of_user:
            return ValidationError('~ email already exists ~')


class FormCreateNewPost(FlaskForm):
    text = StringField('Texto da postagem', widget=TextArea(), validators=[DataRequired()])
    photo = FileField('Imagem', validators=[DataRequired()])
    btn = SubmitField('Publicar')


class FollowForm(FlaskForm):
    user_id = HiddenField('user_id')
    user_follow_id = HiddenField('user_follow_id')
    submit = SubmitField('Seguir')

class LikeForm(FlaskForm):
    post_id = HiddenField('post_id')
    user_id = HiddenField('user_id')
    submit = SubmitField('Seguir')

class FormUpdateUser(FlaskForm):
    username = StringField('Nome Completo', validators=[DataRequired()])
    profile_img = FileField('Imagem de Perfil')
    btn = SubmitField('Atualizar')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comentário')
    submit = SubmitField('Enviar')
