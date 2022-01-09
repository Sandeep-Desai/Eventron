from loginSys import db,login_manager
from datetime import datetime
from flask_login import UserMixin
# from loginSys.routes import receivers

@login_manager.user_loader
def load_user(user_id):
       return User.query.get(int(user_id))




class User(db.Model,UserMixin):
       
       id=db.Column(db.Integer,primary_key=True)
       
       username=db.Column(db.String(20),nullable=False)
       image_profile=db.Column(db.String(20),default="default.jpg",nullable=False)
       email=db.Column(db.String(50),nullable=False)
       password=db.Column(db.String(50),nullable=False)
       # posts=db.relationship("post",backref="author",lazy=True)
       
       def __repr__(self):
              return f"{self.username},{self.email},{self.password},{self.image_profile}"


class Event(db.Model):
       id=db.Column(db.Integer,primary_key=True)
       event_name=db.Column(db.String,nullable=False)
       event_code=db.Column(db.String(20),nullable=False)
       event_members=db.Column(db.String,nullable=False)
       event_admin=db.Column(db.String,nullable=False)

class Task(db.Model):
       id=db.Column(db.Integer,primary_key=True)
       assigned_to=db.Column(db.String,nullable=False)
       task_given=db.Column(db.String,nullable=False)
       eventname=db.Column(db.String,nullable=False)

       
       
