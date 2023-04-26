from flask import Flask, json,redirect,render_template,flash,request
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user

# from flask_mail import Mail
import json


# mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="aneesrehmankhan"


# with open('config.json','r') as c:
#     params=json.load(c)["params"]



# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME='gmail account',
#     MAIL_PASSWORD='gmail account password'
# )
# mail = Mail(app)



# this is for getting the unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databsename'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/carbon'
db=SQLAlchemy(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))


class emission(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    elecemmision=db.Column(db.Integer)
    femmision=db.Column(db.Integer)
    temmsion=db.Column(db.Integer)
    userid=db.Column(db.Integer)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    password=db.Column(db.String(100))
    email=db.Column(db.String(100))


"""HOME"""


@app.route("/")
def home():
  return render_template("signup.html")
  """if request.method=="POST":
        user=request.form.get("username")
        password=request.form.get("password")
        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`password`) VALUES ('{user}','{password}')") 
        return render_template("index.html")"""
    



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        user=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`password`,`email`) VALUES ('{user}','{password}','{email}')") 
        return render_template("signin.html")
    return render_template("signup.html")


#task link route

@app.route("/profile")
def profile():
    return render_template("profile.html",username=current_user.username)

@app.route("/meat")
def meat():
    return render_template("meat.html")
@app.route("/diet")
def diet():
    return render_template("diet.html")
@app.route("/lunch")
def lunch():
    return render_template("lunch.html")
@app.route("/lower")
def lower():
    return render_template("lower.html")
@app.route("/local")
def local():
    return render_template("local.html")
@app.route("/bio")
def bio():
    return render_template("bio.html")
@app.route("/waste")
def waste():
    return render_template("waste.html")
@app.route("/talk")
def talk():
    return render_template("talk.html")
@app.route("/task")
def task():
    return render_template("task.html")

@app.route("/main")
def hom():
    return render_template("homehome.html")

@app.route("/reducef")
def redf():
    id=current_user.id
    val=list(emission.query.with_entities(emission.femmision).filter_by(userid=id).first())
    newval=val[0]-2
    new_user=db.engine.execute(f"UPDATE `emission` set femmision={newval} where(userid={current_user.id})")
    return render_template("homehome.html")
@app.route("/reducet")
def redt():
    id=current_user.id
    val=list(emission.query.with_entities(emission.temmsion).filter_by(userid=id).first())
    newval=val[0]-2
    new_user=db.engine.execute(f"UPDATE `emission` set temmision={newval} where(userid={current_user.id})")
    return render_template("homehome.html")
@app.route("/reduceel")
def redele():
    id=current_user.id
    val=list(emission.query.with_entities(emission.elecemmision).filter_by(userid=id).first())
    newval=val[0]-2
    new_user=db.engine.execute(f"UPDATE `emission` set elecemmision={newval} where(userid={current_user.id})")
    return render_template("homehome.html")
@app.route("/progress")
@login_required
def progress():
    id=current_user.id
    val3=list(emission.query.with_entities(emission.elecemmision).filter_by(userid=id).first())
    val1=list(emission.query.with_entities(emission.temmsion).filter_by(userid=id).first())
    val2=list(emission.query.with_entities(emission.femmision).filter_by(userid=id).first())
    
    return render_template("progress.html",value1=val1[0],value2=val2[0],value3=val3[0])

@app.route("/blogs")
def blog():
    return render_template("main.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        us=request.form.get("username")
        password=request.form.get("password")
        """us=User.query.filter_by(username=us).first()"""
        u=User.query.with_entities(User.username).filter_by(username=us).first()
        ex=User.query.with_entities(User.password).filter_by(username=us).first()
        print(u)
        print(ex[0])
        if ex[0]==password:
            login_user(User.query.filter_by(username=us).first())
            id=current_user.id
            
            if emission.query.with_entities(emission.elecemmision).filter_by(userid=id).first()==None:
                return render_template("form.html")
            else:
                return render_template("homehome.html")
            """return render_template("homehome.html")"""
        else:
            flash("Invalid Credentials","danger")
            return render_template("signin.html")
    return render_template("signin.html")


@app.route("/calculate",methods=['POST','GET'])
def calc():
    if request.method=="POST":
        #get value for transport
        walk=int(request.form.get("Walk"))
        bus=int(request.form.get("Bus"))
        train=int(request.form.get("Train"))
        plane=int(request.form.get("Plane"))
        bike=int(request.form.get("Bike"))
        car=int(request.form.get("Car"))
        #get value for electricity
        ebill=int(request.form.get("bill"))
        #get value for food
        value=int(request.form.get("Food"))
        if value==1:
            fmi=14.5
        elif value==2:
            fmi=10.6
        elif value==3:
            fmi=8.9
        elif value==4:
            fmi=7.6
        elif value==5:
            fmi=2.9
        else:
            fmi=2.5
        foodv=int(request.form.get("foodv"))
        #calc for transportation in kg
        transportemmision=int(((car/0.6213)*404+(bus/0.6213)*68+(train/0.6213)*23+(plane/0.6213)*223+(bike/0.6213)*10)/1000)
        #calc for electricity in kg
        electricityemmision=int((ebill/7)*0.82)
        #calc for food in kg
        foodemmision=int((foodv/1000)*fmi)
        new_user=db.engine.execute(f"INSERT INTO `emission` (`userid`,`temmsion`,`elecemmision`,`femmision`) VALUES ('{current_user.id}','{transportemmision}','{electricityemmision}','{foodemmision}')")
        return render_template("homehome.html")
    return render_template("homehome.html")
@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return f'MY DATABASE IS CONNECTED'
    except Exception as e:
        print(e)
        return f'MY DATABASE IS NOT CONNECTED {e}'
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

app.run(debug=True)