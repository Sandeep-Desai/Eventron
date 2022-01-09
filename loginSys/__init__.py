from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
# from form import registrationForm,loginForm
app=Flask(__name__)
socketio=SocketIO(app)
app.config["SECRET_KEY"]="dkdhsaodoiandonsaofnjdsv2324254y457"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
# app.config["MAIL_USE_TLS"]=True
# app.config["MAIL_USE_SSL"]=False
# app.config["MAIL_DEFAULT_SENDER"]="sandeeptdesai05@gmail.com"
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = "465"
# app.config['MAIL_USERNAME'] = 'Sandeep Desai'
# app.config['MAIL_PASSWORD'] = "desaisandeep@02"


# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = False
# app.config.update()

# app.config["DEBUG"]=True






db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
from loginSys import routes