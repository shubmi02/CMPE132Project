from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __repr__(self):
        return f"Name : {self.firstname}, id: {self.id}"
with app.app_context():
    db.create_all()
    

@app.route("/")
def home():
    return "Placeholder"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']

        new_user = Users(firstname = firstname, lastname = lastname, password = password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        pass

    return render_template("login.html")

