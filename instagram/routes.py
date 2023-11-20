# Aqui vai as rotas e links
import os
import base64
from datetime import datetime

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from instagram.models import load_user, User, Posts, Follows, LikesPost, CommetsPost
from instagram import app, database
from instagram.forms import FormLogin, FormCreateNewAccount, FormCreateNewPost, FollowForm, LikeForm, FormUpdateUser
from instagram import bcrypt
from instagram import login_manager


@app.route('/', methods=['POST', 'GET'])
def login():
    formLogin = FormLogin()

    if formLogin.validate_on_submit():
        userToLogin = User.query.filter_by(email=formLogin.email.data).first()
        if userToLogin and bcrypt.check_password_hash(userToLogin.password, formLogin.password.data):
            login_user(userToLogin)
            return redirect(url_for('homepage'))
        else:
            formLogin.email.errors.append('Email ou senha incorretos')
            return render_template("login.html", teto='LOGIN', form=formLogin)


    return render_template("login.html", teto='LOGIN', form=formLogin)


@app.route('/create_account', methods=['POST', 'GET'])
def create():
    formCreateAccount = FormCreateNewAccount()

    if formCreateAccount.validate_on_submit():
        password = formCreateAccount.password.data
        password_cr = bcrypt.generate_password_hash(password)

        _user_img = formCreateAccount.profile_img.data

        if _user_img:
            # Leia a imagem como bytes e converta para base64
            img_data = base64.b64encode(_user_img.read()).decode('utf-8')
        else:
            img_data = None

        # verificar se já existe o email cadastrado e retornar um erro
        user = User.query.filter_by(email=formCreateAccount.email.data).first()
        if user:
            formCreateAccount.email.errors.append('Email já cadastrado')
            return render_template("create_account.html", form=formCreateAccount)


        newUser = User(
            username=formCreateAccount.username.data,
            email=formCreateAccount.email.data,
            password=password_cr,
            profile_img=img_data or 'https://cdn1.iconfinder.com/data/icons/user-pictures/100/unknown-512.png'
        )

        database.session.add(newUser)
        database.session.commit()
        login_user(newUser, remember=True)
        return redirect(url_for('homepage'))

    return render_template("create_account.html", form=formCreateAccount)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/comments/<int:post_id>', methods=['GET'])
@login_required
def getcomments(post_id):
    comments = CommetsPost.query.filter_by(post_id=post_id).all()

    return jsonify({'comments': [comment.serialize() for comment in comments]})


    # Função para verificar se um usuário está sendo seguido pelo usuário logado
def is_following(user):
    return Follows.query.filter_by(user_id=current_user.id, user_follow_id=user.id).first() is not None


@app.route('/home', methods=['POST', 'GET'])
@login_required
def homepage():
    formCreateNewPost = FormCreateNewPost()

    if formCreateNewPost.validate_on_submit():
        # pegar a img
        _post_img = formCreateNewPost.photo.data

        if _post_img:
            # Leia a imagem como bytes e converta para base64
            img_data = base64.b64encode(_post_img.read()).decode('utf-8')
        else:
            img_data = None

        # criar um obj Post
        newPost = Posts(post_text=formCreateNewPost.text.data,
                       post_img=img_data,
                       user_id=int(current_user.id))
        # salvar no banco
        database.session.add(newPost)
        database.session.commit()

        formCreateNewPost.text.data = ''
        formCreateNewPost.photo.data = None

         # Exibir aviso de sucesso
        flash('Post cadastrado com sucesso!', 'success')

        # Redirecionar para evitar envios duplicados ao recarregar a página
        return redirect(url_for('homepage'))

    users = User.query.where(User.id != current_user.id).order_by(User.id.desc()).all()
    posts = Posts.query.order_by(Posts.id.desc()).all()

     # Adiciona a informação de "Seguindo" ou "Não Seguindo" para cada usuário
    users_with_follow_status = [{'user': user, 'following': is_following(user)} for user in users]

    # users = User.query.all()
    return render_template("home.html", users=users_with_follow_status, posts=posts, form=formCreateNewPost)




@app.route('/follow', methods=['POST'])
def follow():
    form = FollowForm(request.form)

    if form.validate_on_submit():

        is_following = Follows.query.filter_by(user_id=form.user_id.data, user_follow_id=form.user_follow_id.data).first()

        if is_following:
            database.session.delete(is_following)
            database.session.commit()
            return redirect(url_for('homepage'))


        newfollow = Follows(user_id=form.user_id.data,
                       user_follow_id=form.user_follow_id.data,)
        
        # salvar no banco
        database.session.add(newfollow)
        database.session.commit()
      
    return redirect(url_for('homepage'))


@app.route('/like', methods=['POST'])
def like():
    form = LikeForm(request.form)

    is_liked = LikesPost.query.filter_by(user_id=form.user_id.data, post_id=form.post_id.data).first()

    if is_liked:
        database.session.delete(is_liked)
        database.session.commit()
        return redirect(url_for('homepage'))

    if form.validate_on_submit():
        newfollow = LikesPost(user_id=form.user_id.data,
                       post_id=form.post_id.data,)
        
        # salvar no banco
        database.session.add(newfollow)
        database.session.commit()
      
    return redirect(url_for('homepage'))

@app.route('/profile/<user_id>', methods=['POST', 'GET'])
@login_required
def profile(user_id):
    _updateUser = FormUpdateUser()

    if request.method == 'POST' and _updateUser.validate():
        # Obtenha o objeto do banco de dados que você deseja atualizar
        user_to_update = User.query.get(int(user_id))

         # pegar a img
        _user_img = _updateUser.profile_img.data

        if _user_img:
            # Leia a imagem como bytes e converta para base64
            img_data = base64.b64encode(_user_img.read()).decode('utf-8')
        else:
            img_data = None

        # Atualize os atributos do objeto com os novos valores
        user_to_update.username = _updateUser.username.data
        user_to_update.profile_img = img_data

        # Faça o commit para persistir as mudanças no banco de dados
        database.session.commit()

        return redirect(url_for('homepage'))
    
    _user = User.query.get(int(user_id))
    _updateUser.username.data = _user.username

    return render_template("profile.html", user=_user, form=_updateUser)






