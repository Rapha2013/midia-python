from instagram import app, database
from instagram.models import User, Posts
from werkzeug.security import generate_password_hash

# Ative o contexto do aplicativo
app.app_context().push()

# Crie instâncias de usuários e posts
user1 = User(username='user1', email='user1@example.com', password=generate_password_hash('password1'))
user2 = User(username='user2', email='user2@example.com', password=generate_password_hash('password2'))

post1 = Posts(post_text='This is post 1', user=user1)
post2 = Posts(post_text='This is post 2', user=user2)

# Adicione usuários e posts ao banco de dados
database.session.add(user1)
database.session.add(user2)
database.session.add(post1)
database.session.add(post2)

# Commit para salvar as alterações
database.session.commit()

print("Dados adicionados ao banco de dados.")