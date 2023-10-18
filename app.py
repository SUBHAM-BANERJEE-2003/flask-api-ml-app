from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template('index.html')

@app.route("/about")
def aboutPage():
    return render_template('about.html');

@app.route("/login")
def loginPage():
    return render_template('login.html');

@app.route("/register")
def registerPage():
    return render_template('register.html');

if __name__ == '__main__':
    app.run(debug=True)

