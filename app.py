from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __repr__(self):
        return '<id %r>' %self.id
    
    


@app.route("/")
def home():
    return "Placeholder"

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/login")
def login():
    return render_template("login.html")

