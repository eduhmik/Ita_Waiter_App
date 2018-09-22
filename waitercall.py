from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from mockdbhelper import MockDBHelper as DBHelper
from user import User
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper
from forms import RegistrationForm
import config
import datetime

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY = 'AfblyuUyKV5KuvD4uWfOLwnG3nkkEIxKj0Nt6k/dfh9TDcvwKqvBbmXfLirbntA2FM2s8wjURwt2L5OgF/TpHBpz5EADo6ZpWzR'
))
login_manager = LoginManager(app)


@app.route('/')
def home():
    registrationform = RegistrationForm()
    return render_template('home.html', registrationform = registrationform)

@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    print(email)
    password = request.form.get("password")
    print(password)
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    email = request.form.get("email")
    pwd1 = request.form.get("password")
    pwd2 = request.form.get("password2")
    if not pwd1 == pwd2:
        return redirect(url_for('home'))
    if form.validate():
        if DB.get_user(email):
            form.email.errors.append("Email address already registered")
            return render_template('home', registrationform=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(str(pwd1) + str(salt))
        DB.add_user(email, salt, hashed)
        return redirect(url_for('home'))
    return render_template("home.html", registrationform=form)

@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    print(requests)
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds/60), str(deltaseconds % 60).zfill(2))
    return render_template("dashboard.html", requests=requests)

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    tablename = request.form.get("tablenumber")
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = config.base_url + "newrequest/" + tableid
    DB.update_table(tableid, new_url)
    return redirect(url_for('account'))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('account'))

@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request has been received and a waiter will attend you shortly"

@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)