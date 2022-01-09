from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField, SelectMultipleField
from wtforms.validators import data_required,Length,email, EqualTo,email_validator,Email,ValidationError
from loginSys.models import User

class registrationForm(FlaskForm):
    username=StringField("User Name", validators=[data_required(),Length(min=2,max=20)])
    email=StringField("Email", validators=[data_required(),Email()])
    password=PasswordField("Password",validators=[data_required()])
    confirm_password=PasswordField("Confirm Password",validators=[data_required(),EqualTo("password")])
    submit=SubmitField("Sign Up")
    
    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("This email address already exists")

    # def validate_email(self,email):
    #     if email:
    #         raise ValidationError("This is email is already registered")
        
class loginForm(FlaskForm):
    # username=StringField("User Name", validators=[data_required(),Length(min=5,max=25)])
    email=StringField("Email", validators=[data_required(),Email()])
    password=PasswordField("Password",validators=[data_required()])
    remember=BooleanField("Remember me")
    # confirm_password=PasswordField("Confirm Password",validators=[data_required(),EqualTo("password")])
    submit=SubmitField("Log In")
    # def validate_email(self,email):
    #     email=User.query.filter_by(email=email.data).first()
    #     if not email:
    #         raise ValidationError("This email address already exists")


class eventForm(FlaskForm):
    event_name=StringField("User Name", validators=[data_required()])
    event_code=PasswordField("Password",validators=[data_required()])
    confirm_code=PasswordField("Confirm Password",validators=[data_required(),EqualTo("event_code")])
    # admin_mail=StringField("Email", validators=[data_required(),Email()])
    admin_password=PasswordField("Password",validators=[data_required()])
    email=StringField("Emails", validators=[data_required()]) 
    submit=SubmitField("Invite")
    def validate_eventname(self,event_name):
        user=User.query.filter_by(event_name=event_name.data).first()
        if user:
            raise ValidationError("This Eventname already exists")
      
class loginEventform(FlaskForm):
    # email=StringField("Email", validators=[data_required(),Email()])
    event_name=StringField("User Name", validators=[data_required()])
    event_code=PasswordField("Password",validators=[data_required()])
    submit=SubmitField("Log in")


class assignTask(FlaskForm):
    member_email=StringField("Email", validators=[data_required(),Email()])
    taskToAssign=StringField("task", validators=[data_required()])
    submit=SubmitField("Assign") 