from wakuwaku.api import bp

from wakuwaku.models import Comment
from wakuwaku.extensions import db

from flasgger import swag_from

from flask import request, jsonify
from flask_login import login_required, current_user

specs_dict = {
    "definitions": {
        "Comment": {
            "type": "object",
            "properties": {
                "comment_id": {
                    "type": "integer",
                    "description": "The comment ID.",
                    "example": 123
                },
                "post_id": {
                    "type": "integer",
                    "description": "The post ID.",
                    "example": 123
                },
                "account_id": {
                    "type": "integer",
                    "description": "The account ID.",
                    "example": 123
                },
                "content": {
                    "type": "string",
                    "description": "The comment content.",
                    "example": "This is a comment."
                },
                "created_at": {
                    "type": "string",
                    "description": "The date and time the comment was created.",
                    "example": "Wed, 01 Jan 2020 00:00:00 GMT"
                },
            }
        }
    }
}

@bp.route("/comments", methods=["GET"])
@swag_from(specs_dict)
def get_comments():
    """Get comments.

    This endpoint allows users to retrieve all comments.
    
    ---
    tags:
        - comments
    parameters:
        -   name: post_id
            in: query
            type: integer
            required: true
            description: The post ID.
        -   name: page
            in: query
            type: integer
            required: true
            description: The page number.
        -   name: per_page
            in: query
            type: integer
            required: true
            description: The number of comments per page.
    responses:
        200:
            description: Comments found.
            schema:
                type: array
                items:
                    $ref: "#/definitions/Comment"
        400:
            description: Invalid parameters
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: An error message.
                        example: invalid parameters
    """
    try:
        post_id = int(request.args.get("post_id"))
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))
    except (TypeError, ValueError):
        return jsonify({"message": "invalid parameters"}), 400

    comments = Comment.query.filter_by(post_id=post_id).limit(per_page).offset((page - 1) * per_page).all()
    comments = [comment.to_dict() for comment in comments]
    return jsonify(comments), 200

@bp.route("/comments", methods=["POST"])
@login_required
def create_comment():
    """Create a comment.

    This endpoint allows users to create a comment.
    
    ---
    tags:
        - comments
    parameters:
        -   name: post_id
            in: formData
            type: integer
            required: true
            description: The post ID.
        -   name: content
            in: formData
            type: string
            required: true
            description: The comment content.
    responses:
        201:
            description: Comment created.
            schema:
                $ref: "#/definitions/Comment"
        400:
            description: Invalid parameters
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: An error message.
                        example: invalid parameters
    """
    try:
        post_id = int(request.form.get("post_id"))
        content = request.form.get("content")
    except (TypeError, ValueError):
        return jsonify({"message": "invalid parameters"}), 400

    comment = Comment(post_id=post_id, account_id=current_user.account_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201