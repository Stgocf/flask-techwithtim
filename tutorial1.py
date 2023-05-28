from flask import Flask, redirect, url_for, render_template, request, session, flash 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'jahagsft98123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days = 5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.String(30))
    email = db.Column("email", db.String(50))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/test")
def test():
    return render_template("index2.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session['user'] = user

        found_user = users.query.filter_by(name = user).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = users(user, None)
            db.session.add(usr)
            db.session.commit()

        flash('Loggin Successfull!')
        return redirect(url_for("user"))
    else:
        if 'user' in session:
            flash('Already LogIn!')
            return redirect(url_for('user'))
        else:
            flash('You are not LogIn!')
            return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session['user']

        if request.method == "POST":
            email = request.form["email"]
            session['email'] = email
            found_user = users.query.filter_by(name = user).first()
            found_user.email = email
            db.session.commit()
            flash('Email was save correctly!')
        else:
            if 'email' in session:
                email = session['email']

        return render_template("user.html", email=email)
    else:
        flash('You are not log in!')
        return redirect(url_for('login'))
    
@app.route("/view")
def view(): 
    return render_template('view.html', values = users.query.all() )

@app.route("/logout")
def logout():
    if 'user' in session:
        user = session['user']
        flash('you have been logout successfully, {}!'.format(user), 'info')
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)