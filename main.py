"""
pip install..
flask
flask_login
flask_wtf
email_validator
flask_bcrypt
flask_sqlalchemy

"""
from instagram import app, database
from instagram.models import User, Posts

with app.app_context():
    database.create_all()

if __name__ == '__main__':
    app.run(debug=True)


