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
    return User.query.get(int(user_id)) or Hospitaluser.query.get(int(user_id))


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))



class Hospitaluser(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))


class Hospitaldata(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20),unique=True)
    hname=db.Column(db.String(100))
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)

class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20))
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)
    querys=db.Column(db.String(50))
    date=db.Column(db.String(50))



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
    

@app.route("/trigers")
def trigers():
    query=Trig.query.all() 
    return render_template("trigers.html",query=query)


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
def task():
    return render_template("signin.html")
    

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        us=request.form.get("username")
        password=request.form.get("password")
        us=User.query.filter_by(username=us).first()
        ex=User.query.with_entities(User.password).all()
        if list(ex[0])[0]==password:
            login_user(us)
            flash("Login Success","info")
            return render_template("home.html")
        else:
            """ERROR TEXT"""
            flash("Invalid Credentials","danger")
            return render_template("signin.html")
    return render_template("signin.html")
    """srfid=request.form.get('srf')
        dob=request.form.get('dob')
        user=User.query.filter_by(srfid=srfid).first()
        if user and check_password_hash(user.dob,dob):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("userlogin.html")"""

@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return f'MY DATABASE IS CONNECTED'
    except Exception as e:
        print(e)
        return f'MY DATABASE IS NOT CONNECTED {e}'
"""
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addHospitalUser',methods=['POST','GET'])
def hospitalUser():
   
    if('user' in session and session['user']=="admin"):
      
        if request.method=="POST":
            hcode=request.form.get('hcode')
            email=request.form.get('email')
            password=request.form.get('password')        
            encpassword=generate_password_hash(password)  
            hcode=hcode.upper()      
            emailUser=Hospitaluser.query.filter_by(email=email).first()
            if  emailUser:
                flash("Email or srif is already taken","warning")
         
            db.engine.execute(f"INSERT INTO `hospitaluser` (`hcode`,`email`,`password`) VALUES ('{hcode}','{email}','{encpassword}') ")

            # my mail starts from here if you not need to send mail comment the below line
           
            # mail.send_message('COVID CARE CENTER',sender=params['gmail-user'],recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\n\nHospital Code {hcode}\n\n Do not share your password\n\n\nThank You..." )

            flash("Data Sent and Inserted Successfully","warning")
            return render_template("addHosUser.html")

    else:
        flash("Login and try Again","warning")
        return render_template("addHosUser.html")
    


# testing wheather db is connected or not  


@app.route("/logoutadmin")
def logoutadmin():
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect('/admin')


def updatess(code):
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()
    return render_template("hospitaldata.html",postsdata=postsdata)

@app.route("/addhospitalinfo",methods=['POST','GET'])
def addhospitalinfo():
    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    code=posts.hcode
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        hcode=hcode.upper()
        huser=Hospitaluser.query.filter_by(hcode=hcode).first()
        hduser=Hospitaldata.query.filter_by(hcode=hcode).first()
        if hduser:
            flash("Data is already Present you can update it..","primary")
            return render_template("hospitaldata.html")
        if huser:            
            db.engine.execute(f"INSERT INTO `hospitaldata` (`hcode`,`hname`,`normalbed`,`hicubed`,`icubed`,`vbed`) VALUES ('{hcode}','{hname}','{nbed}','{hbed}','{ibed}','{vbed}')")
            flash("Data Is Added","primary")
            return redirect('/addhospitalinfo')
            

        else:
            flash("Hospital Code not Exist","warning")
            return redirect('/addhospitalinfo')




    return render_template("hospitaldata.html",postsdata=postsdata)


@app.route("/hedit/<string:id>",methods=['POST','GET'])
@login_required
def hedit(id):
    posts=Hospitaldata.query.filter_by(id=id).first()
  
    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        hcode=hcode.upper()
        db.engine.execute(f"UPDATE `hospitaldata` SET `hcode` ='{hcode}',`hname`='{hname}',`normalbed`='{nbed}',`hicubed`='{hbed}',`icubed`='{ibed}',`vbed`='{vbed}' WHERE `hospitaldata`.`id`={id}")
        flash("Slot Updated","info")
        return redirect("/addhospitalinfo")

    # posts=Hospitaldata.query.filter_by(id=id).first()
    return render_template("hedit.html",posts=posts)


@app.route("/hdelete/<string:id>",methods=['POST','GET'])
@login_required
def hdelete(id):
    db.engine.execute(f"DELETE FROM `hospitaldata` WHERE `hospitaldata`.`id`={id}")
    flash("Date Deleted","danger")
    return redirect("/addhospitalinfo")


@app.route("/pdetails",methods=['GET'])
@login_required
def pdetails():
    code=current_user.srfid
    print(code)
    data=Bookingpatient.query.filter_by(srfid=code).first()
    return render_template("detials.html",data=data)


@app.route("/slotbooking",methods=['POST','GET'])
@login_required
def slotbooking():
    query1=db.engine.execute(f"SELECT * FROM `hospitaldata` ")
    query=db.engine.execute(f"SELECT * FROM `hospitaldata` ")
    if request.method=="POST":
        
        srfid=request.form.get('srfid')
        bedtype=request.form.get('bedtype')
        hcode=request.form.get('hcode')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        paddress=request.form.get('paddress')  
        check2=Hospitaldata.query.filter_by(hcode=hcode).first()
        checkpatient=Bookingpatient.query.filter_by(srfid=srfid).first()
        if checkpatient:
            flash("already srd id is registered ","warning")
            return render_template("booking.html",query=query,query1=query1)
        
        if not check2:
            flash("Hospital Code not exist","warning")
            return render_template("booking.html",query=query,query1=query1)

        code=hcode
        dbb=db.engine.execute(f"SELECT * FROM `hospitaldata` WHERE `hospitaldata`.`hcode`='{code}' ")        
        bedtype=bedtype
        if bedtype=="NormalBed":       
            for d in dbb:
                seat=d.normalbed
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.normalbed=seat-1
                db.session.commit()
                
            
        elif bedtype=="HICUBed":      
            for d in dbb:
                seat=d.hicubed
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.hicubed=seat-1
                db.session.commit()

        elif bedtype=="ICUBed":     
            for d in dbb:
                seat=d.icubed
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.icubed=seat-1
                db.session.commit()

        elif bedtype=="VENTILATORBed": 
            for d in dbb:
                seat=d.vbed
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.vbed=seat-1
                db.session.commit()
        else:
            pass

        check=Hospitaldata.query.filter_by(hcode=hcode).first()
        if check!=None:
            if(seat>0 and check):
                res=Bookingpatient(srfid=srfid,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone,paddress=paddress)
                db.session.add(res)
                db.session.commit()
                flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                return render_template("booking.html",query=query,query1=query1)
            else:
                flash("Something Went Wrong","danger")
                return render_template("booking.html",query=query,query1=query1)
        else:
            flash("Give the proper hospital Code","info")
            return render_template("booking.html",query=query,query1=query1)
            
    
    return render_template("booking.html",query=query,query1=query1)
"""

app.run(debug=True)