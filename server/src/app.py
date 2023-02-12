import os
import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
  "apiKey": "AIzaSyAeW2e633vAFs4IK6-lN9mjq1VlU0xWYDE",
  "authDomain": "wehack-devtest.firebaseapp.com",
  "databaseURL": "https://wehack-devtest-default-rtdb.firebaseio.com/",
  "storageBucket": "wehack-devtest.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/", methods = ["POST", "GET"])
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup", methods = ["POST", "GET"])
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/quiz", methods = ["POST", "GET"])
def quiz():
    if person["is_logged_in"] == True:
            if request.method == "POST":        #Only if data has been posted
                result = request.form           #Get the data
                val = {"name":person["name"],"uID":person["uid"],"q1":result["q1"],"q2":result["q2"],"q3":result["q3"],"q4":result["q4"]}
                print(val)
                db.child("questions").child(person["uid"]).set(val)
            return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

@app.route("/question", methods = ["POST", "GET"])
def question():
    if person["is_logged_in"] == True:
        return render_template("question.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

@app.route("/welcome", methods = ["POST", "GET"])
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():

    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        #print("email:",email)
        #print("password:",password)
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            
            #Get the name of the user
            data = db.child("users").get()
            
            person["name"] = data.val()[person["uid"]]["name"]

            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except Exception as e:
            #If there is any error, redirect back to login
            print("Exception: ", e)
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            print("1")
            db.child("users").child(person["uid"]).set(data)
            print("Hello")
            #Go to welcome page
            return redirect(url_for('question'))
        except Exception as e:
            #If there is any error, redirect to register
            print("e: ",e)
            return redirect(url_for('signup'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    #app.run()
