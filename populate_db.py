from instagram import app, database
from instagram.models import User, Posts
from werkzeug.security import generate_password_hash
import random


app.app_context().push()

nomes = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Isabel", "Jack"]
sobrenomes = ["Adams", "Brown", "Clark", "Davis", "Evans", "Fisher", "Garcia", "Hill", "Irwin", "Johnson"]

# Criando 10 usuários de exemplo com uma postagem cada
for i in range(1, 11):
    nome = random.choice(nomes)
    sobrenome = random.choice(sobrenomes)
    username = f'{nome.lower()}.{sobrenome.lower()}'
    email = f'{nome.lower()}.{sobrenome.lower()}@example.com'
    password = generate_password_hash('123456')
    
    user = User(username=username, email=email, password=password)
    database.session.add(user)
    database.session.commit()
    
    post_text = f"Olá, eu sou o usuário {username} e esta é a minha primeira postagem!"
    post = Posts(post_text=post_text, user_id=user.id)
    database.session.add(post)
    database.session.commit()


print("Registros de exemplo criados com sucesso!")