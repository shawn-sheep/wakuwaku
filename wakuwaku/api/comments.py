from wakuwaku.api import bp

from wakuwaku.models import Comment, Account
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
                "parent_id": {
                    "type": "integer",
                    "description": "The parent comment ID.",
                    "example": 123
                },
                "account_id": {
                    "type": "integer",
                    "description": "The account ID.",
                    "example": 123
                },
                "avatar": {
                    "type": "string",
                    "description": "The account avatar.",
                    "example": "https://www.google.com"
                },
                "username": {
                    "type": "string",
                    "description": "The account username.",
                    "example": "username"
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
                "replies": {
                    "type": "array",
                    "description": "The replies to the comment.",
                    "items": {
                        "$ref": "#/definitions/Comment"
                    }
                }
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

    # comments = Comment.query.filter_by(post_id=post_id).limit(per_page).offset((page - 1) * per_page).all()
    # comments = [comment.to_dict() for comment in comments]
    # return jsonify(comments), 200

    # 按照created_at排序，最多返回per_page个comment，级联查询replies，一级评论的parent_id为0
    query = '''
WITH RECURSIVE cascaded_comments AS (
  SELECT comment_id, account_id, content, parent_id
  FROM comment
  WHERE comment_id IN (
		SELECT c.comment_id FROM comment c
		WHERE c.post_id = :post_id AND c.parent_id IS NULL
		ORDER BY created_at DESC
		LIMIT :per_page OFFSET :offset
	)

  UNION ALL

  SELECT comment.comment_id, comment.account_id, comment.content, comment.parent_id
  FROM comment
  JOIN cascaded_comments ON comment.parent_id = cascaded_comments.comment_id
)
SELECT cascaded_comments.*, account.avatar_url, account.username
FROM cascaded_comments NATURAL JOIN account
ORDER BY created_at DESC;
    '''
    comments = db.session.execute(query, {"post_id": post_id, "per_page": per_page, "offset": (page - 1) * per_page}).fetchall()
    comments = [dict(comment) for comment in comments]
    # 从每个一级评论开始，递归地添加其子评论
    def add_child_comments(comment):
        comment["replies"] = []
        for c in comments:
            if c["parent_id"] == comment["comment_id"]:
                comment["replies"].append(c)
                add_child_comments(c)
    for comment in comments:
        if comment["parent_id"] == None:
            add_child_comments(comment)
    # 只返回一级评论
    comments = [comment for comment in comments if comment["parent_id"] == None]
    return jsonify(comments), 200

@bp.route("/comment", methods=["POST"])
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
        -   name: parent_id
            in: formData
            type: integer
            required: true
            description: The parent of the comment.
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
        parent_id = int(request.form.get("parent_id"))
        content = request.form.get("content")
    except (TypeError, ValueError):
        return jsonify({"message": "invalid parameters"}), 400

    if parent_id == 0: parent_id = None
    comment = Comment(post_id=post_id, parent_id=parent_id, account_id=current_user.account_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@bp.route("/comment/<int:comment_id>", methods=["PUT"])
@login_required
def update_comment(comment_id):
    """Update a comment.

    This endpoint allows users to update a comment.
    
    ---
    tags:
        - comments
    parameters:
        -   name: comment_id
            in: path
            type: integer
            required: true
            description: The comment ID.
        -   name: content
            in: formData
            type: string
            required: true
            description: The comment content.
    responses:
        200:
            description: Comment updated.
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
        403:
            description: Forbidden
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: An error message.
                        example: forbidden
        404:
            description: Comment not found
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: An error message.
                        example: comment not found
    """
    try:
        content = request.form.get("content")
    except (TypeError, ValueError):
        return jsonify({"message": "invalid parameters"}), 400

    comment = Comment.query.get(comment_id)
    if comment is None:
        return jsonify({"message": "comment not found"}), 404
    if comment.account_id != current_user.account_id:
        return jsonify({"message": "forbidden"}), 403

    comment.content = content
    db.session.commit()
    return jsonify(comment.to_dict()), 200

from sqlalchemy import delete

@bp.route("/comment/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id):
    """Delete a comment.

    This endpoint allows users to delete a comment.
    
    ---
    tags:
        - comments
    parameters:
        -   name: comment_id
            in: path
            type: integer
            required: true
            description: The comment ID.
    responses:
        204:
            description: Comment deleted.
        403:
            description: Forbidden
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: An error message.
                        example: forbidden
        404:
            description: Comment not found
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: An error message.
                        example: comment not found
    """
    comment = Comment.query.get(comment_id)
    if comment is None:
        return jsonify({"message": "comment not found"}), 404
    if comment.account_id != current_user.account_id:
        return jsonify({"message": "forbidden"}), 403

    db.session.execute(delete(Comment).where(Comment.comment_id == comment_id))
    db.session.commit()
    return jsonify({}), 204