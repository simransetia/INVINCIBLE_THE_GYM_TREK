from flask import Flask, render_template, redirect, url_for, request, session, Response
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin
import pandas as pd
import numpy as np
import logging
import datetime
import os.path
from flask import Markup
import os
import cv2
import mediapipe as mp
import pymongo



# def gen_frames():  
#     camera = cv2.VideoCapture(0)
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


app=Flask(__name__)
app.config["DEBUG"]= True


client = pymongo.MongoClient("mongodb+srv://admin_simran:<password>@cluster0.r9se2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database("total_records")
records = db.register


@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('home.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('home.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('home.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            return render_template('index.html', email=new_email)
    return render_template('home.html')
@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('index.html', email=email)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

# @app.route('/',methods=["POST","GET"])
# def home():
#
#     return render_template("index.html")

@app.route('/squats',methods=["POST","GET"])
def squats():
    count=0
    calories=0
    from squats import squats
    if request.method=="POST":
        n=request.form.get('co')
        count,calories = squats(int(n))
    

    return render_template('squats.html',count = count,calories = calories)

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pushup',methods=["POST","GET"])
def pushups():
    count=0
    calories=0
    if request.method=="POST":
        from push_up import pushup
        print("started")
        n=request.form.get('co')
        print(n)
        count,calories = pushup(int(n))
    
    return render_template('pushup.html',count = count,calories = calories)

@app.route('/pullup',methods=["POST","GET"])
def pullup():
    count=0
    calories=0
    if request.method=="POST":
        from pull_up import pullup
        print("started")
        n=request.form.get('co')
        print(n)
        count,calories = pullup(int(n))
    
    return render_template('pullup.html',count = count,calories = calories)

@app.route('/biceps',methods=["POST","GET"])
def biceps():
    
    count=0
    calories=0
    if request.method=="POST":
        from weight_lifting import biceps
        print("started")
        n=request.form.get('co')
        print(n)
        count,calories = biceps(int(n))
    
    return render_template('weight_lifting.html',count = count,calories = calories)


@app.route('/crunches',methods=["POST","GET"])
def crunches():
    
    count=0
    calories=0
    if request.method=="POST":
        from crunches import crunches
        print("started")
        n=request.form.get('co')
        print(n)
        count,calories = crunches(int(n))
    
    
    return render_template('crunches.html',count = count,calories = calories)

@app.route('/count',methods=["POST","GET"])
def count():
    return render_template('count.html')

if __name__ == '__main__': 

    app.run()
