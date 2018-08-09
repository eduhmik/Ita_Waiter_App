from flask import Flask, render_template
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user

from mockdbhelper import MockDBHelper as DBHelper
from user import User

from flask import redirect
from flask import url_for
from flask import request
DB = DBHelper()

app = Flask(__name__)
app.secret_key = 'AfblyuUyKV5KuvD4uWfOLwnG3nkkEIxKj0Nt6k/dfh9TDcvwKqvBbmXfLirbntA2FM2s8wjURwt2L5OgF/TpHBpz5EADo6ZpWzR'
login_manager = LoginManager(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/account")
@login_required
def account():
    return "You are logged in"

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = DB.get_user("email")
    if user_password == password:
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)