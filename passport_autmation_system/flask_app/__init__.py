import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)

app.config['SECRET_KEY'] = '4aa4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= '587'
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME']= 'yourmail@gmail.com'
app.config['MAIL_PASSWORD']= 'yourpassword'
mail = Mail(app)


from flask_app import routes