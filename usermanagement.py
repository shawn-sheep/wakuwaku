from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from model import db, app, Account


from flask import request, redirect, url_for
from flask_login import login_user, logout_user, login_required


@app.route("/register", methods=["POST"])
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    user = Account()
    user.username = username
    user.email = email
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("login"))


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = Account.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return "Invalid username or password"

    login_user(user)

    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)