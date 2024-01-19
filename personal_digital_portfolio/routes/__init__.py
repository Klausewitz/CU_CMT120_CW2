from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# main app for flask
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static',
            static_url_path='/static'
            )


# database server information
USERNAME = 'root'
PASSWORD = 'Admin123456'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'blog_db'


app.config['SECRET_KEY'] = 'dQw4w9WgXcQ'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'


db = SQLAlchemy(app)
login_manager = LoginManager(app)


# import from admin.py and users.py             
from routes import admin
from routes import guest