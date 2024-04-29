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
    role = db.Column(db.String(100), default='user')
    authenticate = db.Column(db.Boolean, default=False)  

    def __init__(self, email, password, name, role='user', authenticate = False):  
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.authenticate = authenticate

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"Name: {self.name}, ID: {self.id}, Role: {self.role}"

    
with app.app_context():
    db.create_all()

def load_user(user_id):
    return Users.query.filter_by(username=user_id).first()

def load_all_users():
    return Users.query.all()

def is_authorized(required_role):
    email = session.get('email')
    if not email:
        return False
    user = Users.query.filter_by(email=email).first()
    if user and user.role == required_role and user.authenticate == True:
        return True
    return False

@app.route("/admin", methods=['GET', 'POST'])
@app.route("/admin", methods=['GET', 'POST'])
def admin_dashboard():
    if not is_authorized('employee'):
        return redirect('/login')
    
    if request.method == 'POST':
        # This handles the form submission for updating authentication status
        for key, value in request.form.items():
            if key.startswith('authentication-'):
                user_id = int(key.split('-')[1])
                authenticate_value = value == 'True'
                user = Users.query.get(user_id)
                if user:
                    user.authenticate = authenticate_value

            elif key.startswith('role-'):
                user_id = int(key.split('-')[1])
                user = Users.query.get(user_id)
                if user:
                    user.role = value

        db.session.commit()       
        return redirect('/admin')
    
    users = load_all_users()
    
    # Fetch all unique roles from the database
    roles = db.session.query(Users.role).distinct().all()
    roles = [role[0] for role in roles]

    return render_template('admin.html', userlist=users, roles=roles)


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
        role = request.form['role']

        new_user = Users(name = name, email = email, password = generate_password_hash(password), role = role)
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
            session['role'] = user.role
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

