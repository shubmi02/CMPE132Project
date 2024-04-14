from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init(self, email,password, name):
        self.name = name
        self.email = email
        self.password = password

    def check_password(self,password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"Name : {self.firstname}, id: {self.id}"
    
with app.app_context():
    db.create_all()
    

@app.route("/")
def home():
    # if session['name']:
    return "Placeholder"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = Users(name = name, email = email, password = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/')
        
        else:
            return render_template('login.html', error="Invalid User")

    return render_template('login.html')

