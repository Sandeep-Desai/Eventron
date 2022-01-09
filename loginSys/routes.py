from flask import render_template,flash,redirect,request
from loginSys.form import registrationForm,loginForm,eventForm,loginEventform,assignTask
from loginSys.models import User,Event,Task
from loginSys import app,db,bcrypt,socketio
from flask_login import login_user
import smtplib
from flask_socketio import send
@app.route("/")
def home():
   
   # mail.send_message("Hey there", recipients=["desai.sandeep@iitgn.ac.in"])
   
   return redirect("/loginForm")




@app.route('/registration',methods=["GET","POST"] )
def register():
   form=registrationForm()
   # print(form.validate_on_submit)
   if form.validate_on_submit():
      # flash(f"Account was created successfully and now you can login","green")
      hashed_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
      user=User(username=form.username.data,password=hashed_password,email=form.email.data)
      db.session.add(user)
      db.session.commit()
      return redirect("/loginForm")                    
   else:
      
      return render_template("register.html",form=form,title="Register")
      flash(f"Something went wrong, please check that email and password are valid","red")

@app.route('/loginForm',methods=["GET","POST"])
def login():
   form=loginForm()
   if form.validate_on_submit():
          user=User.query.filter_by(email=form.email.data).first()
          if user and bcrypt.check_password_hash(user.password,form.password.data):
                 login_user(user,remember=form.remember.data)
                 return redirect("/userpage/"+str(user.id))
          else:      
            flash("Login Unsuccesful please check email and password",category="red")
   return render_template("login.html",form=form,title="Log In")

@app.route("/userpage/<int:id>")
def show_userpage(id):
       user=User.query.get(id)
       return render_template("homepage.html",user=user)


@app.route('/createEvent/<int:id>',methods=["GET","POST"] )
def create_event(id):
   form=eventForm()
   # print(form.validate_on_submit)
   if form.validate_on_submit():
      # flash(f"Account was created successfully and now you can login","green")
      
      
      user=User.query.get(id)
             
      code=form.event_code.data
      members=form.email.data
      membesr_sep=members.split(",")
      # admin_mail=form.admin_mail.data
      event=Event(event_name=form.event_name.data,event_code=code,event_members=form.email.data,event_admin=user.email)
      db.session.add(event)
      db.session.commit()
      with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(user.email,form.admin_password.data)
        subject=f"Invitation to Collabrate in {form.event_name.data}"
        body=f"You are Invited to Collabrate in {form.event_name.data} and your code to login in the event is {form.event_code.data}"  
        msg=f"Subject: {subject}\n\n{body}"
        for email in membesr_sep:
           smtp.sendmail(user.email,email,msg)
      return redirect("/loginInEvent/"+str(user.id))
        
      # db.session.commit()
                        
   else:
      user=User.query.get(id)
      return render_template("createEvent.html",form=form,user=user)

@app.route("/loginInEvent/<int:id>",methods=["GET","POST"])
def loginEvent(id):
   form=loginEventform()
   user=User.query.get(id)
   if form.validate_on_submit():
          event=Event.query.filter_by(event_name=form.event_name.data).first()
          
          a=0
          
          if ((event) and (form.event_code.data==event.event_code)):
            memberlist=event.event_members.split(",")
            for email in memberlist:
                 if email==user.email:
                        a=a+1
            if a>0:
               return redirect("/eventpage/"+str(event.id)+"/"+str(user.id))
            else:
                   flash("You are not the part of this event team",category="red")
                   render_template("loginevent.html",form=form,title="Log In")
          else:      
            flash("Login Unsuccesful please check if you have entered a valid event name and code",category="red")
   return render_template("loginevent.html",form=form,title="Log In")
tasks=[]
@app.route("/eventpage/<int:eventid>/<int:userid>", methods=["GET","POST"])
def show_event(eventid,userid):
   # form=assignTask()
   event=Event.query.get(eventid)
   user=User.query.get(userid)
   
   # if form.validate_on_submit():
   #        task=Task(assigned_to=form.member_email.data,task_given=form.taskToAssign.data)
   all_tasks=Task.query.all()
   #        tasks.append([form.member_email.data,form.taskToAssign.data])
         #  return render_template("eventpage.html", event=event,is_admin=a,form=form,tasks=tasks)
   if request.method=="POST":
         #  tasks.append([request.form["email"],request.form["task"]])
          task=Task(assigned_to=request.form["email"],task_given=request.form["task"],eventname=event.event_name)
          db.session.add(task)
          
          db.session.commit()
          return redirect("/eventpage/"+str(eventid)+"/"+str(userid))
   
   a="false"
   if event.event_admin==user.email:
          a="true"
   else:
          a="false"
   return render_template("eventpage.html", event=event,is_admin=a,tasks=all_tasks)
@socketio.on("message")
def messages(msg):
       send(msg,broadcast=True)
