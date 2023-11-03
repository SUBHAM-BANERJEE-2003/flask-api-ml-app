from flask import Flask, render_template, flash, redirect, url_for,request,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email, NumberRange, EqualTo
from flask_bcrypt import Bcrypt
from model import RealEstateModel

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/realestate'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretpassword'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True) 
    password = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    
    def __repr__(self) -> str:
        return '<Name %r>' % self.username


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    re_password = PasswordField('Re-enter Password', validators=[InputRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[NumberRange(min=1, max=125)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Enter Username"})
     email = EmailField(validators=[InputRequired(), Email()], render_kw={"placeholder": "Enter your email"})
     password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Password"})
     submit = SubmitField('Submit')

class predictionForm(FlaskForm):
    baths = IntegerField('Bathrooms', validators=[NumberRange(min=1, max=100)])
    balcony = SelectField('Property Type', choices=[
    (0, 'No'),
    (1, 'Yes'),
])
    total_area = IntegerField('Total Area', validators=[NumberRange(min=1, max=10000)])
    price_per_sqft = IntegerField('Price per sqft', validators=[NumberRange(min=1, max=1000000)])
    city = SelectField('City', choices=[
    (0, 'Bangalore'),
    (1, 'Chennai'),
    (2, 'Delhi'),
    (3, 'Hyderabad'),
    (4, 'Kolkata'),
    (5, 'Mumbai'),
    (6, 'Pune'),
    (7, 'Thane')
])
    property_type = SelectField('Property Type', choices=[
    (0, 'Flat'),
    (1, 'Independent House'),
    (2, 'Villa')
])
    submit = SubmitField('Predict')

@app.route("/")
def homePage():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route("/about")
def aboutPage():
    return render_template('about.html')

@app.route("/login", methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        
        if not existing_user or not existing_email:
            flash('Invalid username or email', 'error')
            return redirect(url_for('loginPage'))

        if bcrypt.check_password_hash(existing_user.password, password):
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('homePage'))
        else:
            flash('Invalid password', 'error')
            return redirect(url_for('loginPage'))

    return render_template('login.html', form=form)

# Add a route to log out
@app.route("/logout")
def logout():
    # Remove the username from the session
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('homePage'))

@app.route("/property")
def propertyPage():
    return render_template('property-grid.html')

@app.route("/register", methods=["GET", "POST"])
def registerPage():
    form = RegisterForm()

    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        age = request.form.get("age")
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash("This username already exists.", "error")
        elif existing_email:
            flash("This email address is already in use.", "error")
        else:
            new_user = User(username=username, email=email, password=hashed_pass, age=age)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for("loginPage"))
    return render_template('register.html', form=form)

def citydecoder(city):
    if city == 0:
        return [1,0,0,0,0,0,0,0]
    elif city == 1:
        return [0,1,0,0,0,0,0,0]
    elif city == 2:
        return [0,0,1,0,0,0,0,0]
    elif city == 3:
        return [0,0,0,1,0,0,0,0]
    elif city == 4:
        return [0,0,0,0,1,0,0,0]
    elif city == 5:
        return [0,0,0,0,0,1,0,0]
    elif city == 6:
        return [0,0,0,0,0,0,1,0]
    else:
        return [0,0,0,0,0,0,0,1]

def propertydecoder(property_type):
    if property_type == 0:
        return [1,0,0]
    elif property_type == 1:
        return [0,1,0]
    else:
        return [0,0,1]

model = RealEstateModel()
@app.route("/predict", methods=["GET", "POST"])
def predictPrice():
    form = predictionForm()
    my_list = []
    if request.method == 'POST':
        baths = int(request.form.get("baths"))
        balcony = int(request.form.get("balcony"))
        total_area = int(request.form.get("total_area"))
        price_per_sqft = int(request.form.get("price_per_sqft"))
        city = int(request.form.get("city"))
        property_type = int(request.form.get("property_type"))
        city_decoded = citydecoder(city)
        my_list = [baths, balcony, total_area, price_per_sqft]
        my_list.extend(city_decoded)
        property_type_decoded = propertydecoder(property_type)
        my_list.extend(property_type_decoded)
        print(my_list)
        prediction = model.predict([my_list])
        finalprediction = prediction[-1]*100000
        print(prediction)
        # return redirect(url_for("homePage"))
    return render_template('predict.html', form=form,prediction_result=finalprediction)
#      data = request.get_json()
#      input_data = data['input_data']
#     # Use the model to make predictions
#      prediction = model.predict(input_data)
#      return jsonify({'prediction': prediction.tolist()})

@app.cli.command("create_tables")
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    create_tables()