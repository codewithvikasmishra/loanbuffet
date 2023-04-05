from typing import Collection
from flask import flash, Flask, render_template, request, jsonify,abort, after_this_request, redirect, url_for, session
from flask_session import Session
import tempfile
from passlib.hash import sha256_crypt
import os
import subprocess
import json
from flask.ctx import after_this_request
import pandas as pd
from connection.db_connect_mongo import *
from config.logger import *
from connection.dbconfig import *

# request is used to get values from HTML form


logger = logging.getLogger('mongodb')
setup_logger(logger,'logs/mongodb/mongodb.logs')

A=Cnxn
mongo_cnxn=A.mongodb_conn()

B=Read_Config()
db_config = B.read_config('mongodb')

app = Flask(__name__) 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = "super secret key"

@app.route('/home', methods = ['GET'])
def gethome():
    return render_template('home1.html')

@app.route('/aboutus')
def getabout():
    return render_template('aboutus.html')

@app.route('/career')
def getcareer():
    return render_template('careers.html')

@app.route('/typeofloan')
def typeofloan():
    return render_template('typeofloan.html')

@app.route('/contactus')
def getcontactus():
    return render_template('contactus.html')

@app.route('/requestform')
def requestform():
    return render_template('userform.html')

@app.route('/requestform',methods = ['GET','POST'])
def requestformpage():
    request_for = request.form['request_for']
    fname = request.form['fname']
    mname = request.form['mname']
    lname = request.form['lname']
    gender = request.form['gender']
    dob = request.form['dob']
    address = request.form['address']
    pincode = request.form['pincode']
    state = request.form['state']
    marital_status = request.form['marital_status']
    email = request.form['email']
    mobile = request.form['mobile']
    salary = request.form['salary']
    liability = request.form['liability']
    dependent = request.form['dependent']

    logger.info("Data fetched from userform")

    record = {'request_raised_for':request_for,
              'fname':fname,
              'mname':mname,
              'lname':lname,
              'gender':gender,
              'dob':dob,
              'address':address,
              'pincode':pincode,
              'state':state,
              'marital_status':marital_status,
              'email':email,
              'mobile':mobile,
              'salary':salary,
              'liability':liability,
              'dependent':dependent}
    
    logger.info("Dictionary created to insert record in mongodb")
    logger.info(record)
    logger.info(mongo_cnxn[2])

    try:
        mongo_cnxn[2].insert_one(record)
        logger.info("Record inserted in mongo db")
    except Exception as e:
        logger.error(f"Some error while inserting the record,{e}")

    # return request_for, fname, mname, lname, gender, dob, address, pincode, state, marital_status,email, mobile, salary, liability, dependent
    return render_template('userform_pass.html', request_for=request_for, fname=fname, mname=mname, lname=lname, gender=gender,
                           dob=dob, address=address, pincode=pincode, state=state, marital_status=marital_status,
                           email=email, mobile=mobile, salary=salary, liability=liability, dependent=dependent)


@app.route('/signup')
def home1():
    return render_template('signup.html')

@app.route('/signup',methods = ['GET','POST'])
def signuppage():
    if request.method=='POST':
        uname = request.form['uname']
        email = request.form['email']
        pwd = request.form['password']
        r_pwd = request.form['repeatPassword']

        logger.info("Data fetched from signup form")

        if pwd!=r_pwd:
            logger.info("Pwd and confirm pwd is same for ", email)
            return "Your pwd and confirm pwd is not same"
        
        else:
            record = {'username':uname,
              'email':email,
              'password':pwd,
              'confirmpwd':r_pwd}
            
            logger.info("Dictionary created to insert record in mongodb")
            
            collection = mongo_cnxn[1][db_config['signup_database']]

            try:
                collection.insert_one(record)
                logger.info("Record inserted in mongo db for signup form")
            except Exception as e:
                logger.error(f"Some error while inserting the record for signup form,{e}")
        return redirect(url_for('loginpage'))
    return redirect(url_for('signuppage'))

@app.route('/index')  
def index():  
    return render_template("index.html")  

@app.route('/login')
def getlogin():
    return render_template('login.html')

@app.route('/login',methods = ['GET','POST'])
def loginpage():
    uname = request.form['uname']
    session['uname'] = uname
    pwd = request.form['pwd']

    error = None

    logger.info("Data fetched from signup form")

    collection = mongo_cnxn[1][db_config['signup_database']]
    query = collection.find({"email":uname})
    for record in query:
        if 'email' in record.keys():
            data = record['password']
            logger.info("Data fetched for pwd matching")

    if pwd != data:
        error = "Invalid Password"
        logger.info("Pwd didn't matched with databse")
    else:
        flash("You are successfully logged in")
        logger.info("Pwd matched with databse")
        return redirect(url_for('userpage'))
    return render_template('login.html', error=error)


# @app.route('/userinfo')
# def getuser():
#     return render_template('userpage.html')

@app.route('/userinfo',methods = ['GET'])
def userpage():
    try:
        query = mongo_cnxn[2].find({"email":session.get('uname')})
        logger.info("email id: ", session.get('uname'))
        for data in query:
            if 'email' in data.keys():
                request_for = data['request_raised_for']
                fname = data['fname']
                mname = data['mname']
                lname = data['lname']
                gender = data['gender']
                dob = data['dob']
                address = data['address']
                pincode = data['pincode']
                state = data['state']
                marital_status = data['marital_status']
                email = data['email']
                mobile = data['mobile']
                salary = data['salary']
                liability = data['liability']
                dependent = data['dependent']
                logger.info("momgo db query ran successfully")
        return render_template('userpage.html', request_for=request_for, fname=fname, mname=mname, lname=lname,
                               gender=gender, dob=dob, address=address, pincode=pincode, state=state, marital_status=marital_status,
                                 email=email, mobile=mobile, salary=salary, liability=liability, dependent=dependent)
    except Exception as e:
        logger.error(f"Some error while fetching data from db or loading data into form")
        return request_for


if __name__== '__main__':
    app.run(debug=True)