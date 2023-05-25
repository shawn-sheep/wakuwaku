from wakuwaku.api import bp
from wakuwaku.models import Account

from wakuwaku.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


from flask import request, jsonify
from flask_login import login_user, logout_user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify({"message": "unauthorized"}), 401


@bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    if username is None or password is None or email is None:
        return jsonify({"message": "username, password and email are required"}), 400

    if Account.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "username already exists"}), 400

    account = Account(username=username, email=email)
    account.set_password(password)

    db.session.add(account)
    db.session.commit()

    return (
        jsonify(
            {"message": "user created successfully", "user_id": account.account_id}
        ),
        201,
    )


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        return jsonify({"message": "username and password are required"}), 400

    account = Account.query.filter_by(username=username).first()

    if account is None or not account.check_password(password):
        return jsonify({"message": "invalid username or password"}), 400

    login_user(account)
    return jsonify({"message": "logged in successfully"}), 200

from flask_login import login_required, current_user

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "logged out successfully"}), 200


@bp.route("/user", methods=["GET"])
@login_required
def get_user_info():
    return (
        jsonify(
            {
                "username": current_user.username,
                "email": current_user.email,
                "created_at": current_user.created_at,
            }
        ),
        200,
    )


@bp.route("/user", methods=["PUT"])
@login_required
def update_user_info():
    username = request.json.get("username")
    email = request.json.get("email")

    if username is not None:
        if Account.query.filter_by(username=username).first() is not None:
            return jsonify({"message": "username already exists"}), 400
        current_user.username = username
    if email is not None:
        if Account.query.filter_by(email=email).first() is not None:
            return jsonify({"message": "email already exists"}), 400
        current_user.email = email

    db.session.commit()
    return jsonify({"message": "user updated successfully"}), 200