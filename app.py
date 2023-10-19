from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretpassword'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=True)

@app.route("/")
def homePage():
    return render_template('index.html');

@app.route("/about")
def aboutPage():
    return render_template('about.html');

@app.route("/login")
def loginPage():
    return render_template('login.html');

@app.route("/register")
def registerPage():
    return render_template('register.html');

def create_tables():
    with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

