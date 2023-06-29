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

@login_manager.request_loader
def load_user_from_request(request):
    # 检查 Authorization Header Bearer
    auth_header = request.headers.get('Authorization')
    if auth_header:
        session_id = auth_header.split(" ")[1]
        # 检查session_id是否存在
        res = login_manager._load_user_from_remember_cookie(session_id)
        print(res)
        return res
    return None

@bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    This endpoint allows users to register by providing a unique username, a password, and an email address.
    
    ---
    tags:
        - users
    parameters:
      - in: body
        name: user
        description: User registration details.
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The desired username for the new user.
            password:
              type: string
              description: The password for the new user.
            email:
              type: string
              description: The email address for the new user.
    responses:
      201:
        description: User created successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: A success message.
              example: user created successfully
            user_id:
              type: integer
              description: The ID of the created user.
              example: 123
      400:
        description: Invalid request or username already exists.
        schema:
          type: object
          properties:
            message:
              type: string
              description: An error message.
    """
    if request.is_json:
        username = request.json.get("username")
        password = request.json.get("password")
        email = request.json.get("email")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

    if username is None or password is None or email is None:
        return jsonify({"message": "username, password and email are required"}), 400

    if Account.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "username already exists"}), 400

    account = Account(username=username, email=email, avatar_url="")
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
    """User login.

    This endpoint allows users to log in by providing their username and password.
    
    ---
    tags:
        - users
    parameters:
      - in: body
        name: credentials
        description: User login credentials.
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The username of the user.
            password:
              type: string
              description: The password of the user.
    responses:
      200:
        description: User logged in successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: A success message.
              example: logged in successfully
      400:
        description: Invalid request or invalid username/password.
        schema:
          type: object
          properties:
            message:
              type: string
              description: An error message.
    """
    if request.is_json:
        username = request.json.get("username")
        password = request.json.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

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
    """User logout.

    This endpoint allows logged-in users to log out.
    
    ---
    tags:
        - users
    responses:
      200:
        description: User logged out successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: A success message.
              example: logged out successfully
    """
    logout_user()
    return jsonify({"message": "logged out successfully"}), 200


@bp.route("/user", methods=["GET"])
@login_required
def get_user_info():
    """Get user information.

    This endpoint allows logged-in users to retrieve their own user information.
    
    ---
    tags:
        - users
    responses:
      200:
        description: User information retrieved successfully.
        schema:
          type: object
          properties:
            username:
              type: string
              description: The username of the user.
            email:
              type: string
              description: The email address of the user.
            created_at:
              type: string
              format: date-time
              description: The creation timestamp of the user.
            avatar_url:
              type: string
              description: The avatar URL of the user.
    """
    return (
        jsonify(
            {
                "account_id": current_user.account_id,
                "username": current_user.username,
                "email": current_user.email,
                "created_at": current_user.created_at,
                "avatar_url": current_user.avatar_url,
            }
        ),
        200,
    )

@bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_info_by_id(user_id):
    """Get user information by ID.

    This endpoint allows users to retrieve user information by ID.
    
    ---
    tags:
        - users
    parameters:
      - in: path
        name: user_id
        description: The ID of the user to retrieve.
        required: true
        schema:
          type: integer
    responses:
      200:
        description: User information retrieved successfully.
        schema:
          type: object
          properties:
            username:
              type: string
              description: The username of the user.
            email:
              type: string
              description: The email address of the user.
            created_at:
              type: string
              format: date-time
              description: The creation timestamp of the user.
            avatar_url:
              type: string
              description: The avatar URL of the user.
      404:
        description: User not found.
        schema:
          type: object
          properties:
            message:
              type: string
              description: An error message.
    """
    account = Account.query.filter_by(account_id=user_id).first()

    if account is None:
        return jsonify({"message": "user not found"}), 404

    return (
        jsonify(
            {
                "account_id": account.account_id,
                "username": account.username,
                "email": account.email,
                "created_at": account.created_at,
                "avatar_url": account.avatar_url,
            }
        ),
        200,
    )

from PIL import Image as PILImage
from wakuwaku.utils import save_file

@bp.route("/user", methods=["PUT"])
@login_required
def update_user_info():
    """Update user information.

    This endpoint allows logged-in users to update their own user information.
    
    ---
    tags:
        - users
    parameters:
      - in: formData
        name: username
        description: The username of the user.
        required: false
        type: string
      - in: formData
        name: email
        description: The email address of the user.
        required: false
        type: string
      - in: formData
        name: avatar
        description: The avatar image of the user.
        required: false
        type: file
    responses:
      200:
        description: User information updated successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: A success message.
              example: user updated successfully
      400:
        description: Invalid request or username/email already exists.
        schema:
          type: object
          properties:
            message:
              type: string
              description: An error message.
              example: username already exists
    """
    username = request.form.get("username")
    email = request.form.get("email")
    avatar = request.files.get("avatar")

    if username is None and email is None and avatar is None:
        return jsonify({"message": "no data provided"}), 400

    if username is not None:
        if Account.query.filter_by(username=username).first() is not None:
            return jsonify({"message": "username already exists"}), 400
        current_user.username = username
    if email is not None:
        if Account.query.filter_by(email=email).first() is not None:
            return jsonify({"message": "email already exists"}), 400
        current_user.email = email
    if avatar is not None:
        thumbnail = PILImage.open(avatar).convert("RGB")
        # 裁剪为正方形
        width, height = thumbnail.size
        length = min(width, height)
        left = (width - length) / 2
        top = (height - length) / 2
        right = (width + length) / 2
        bottom = (height + length) / 2
        thumbnail = thumbnail.crop((left, top, right, bottom))
        
        thumbnail.thumbnail((180, 180))
        avatar_url = save_file(thumbnail, "avatar", 100, f'{current_user.account_id}.jpg')
        current_user.avatar_url = avatar_url
    db.session.commit()
    return jsonify({"message": "user updated successfully"}), 200