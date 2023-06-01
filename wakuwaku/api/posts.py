from wakuwaku.api import bp
from wakuwaku.models import Account, Post, Comment, Vote, Image
from wakuwaku.extensions import db

from flasgger import swag_from

from flask import request, jsonify
from flask_login import login_required

specs_dict = {
    "definitions": {
        "Post": {
            "type": "object",
            "properties": {
                "post_id": {
                    "type": "integer",
                    "description": "The post ID.",
                    "example": 123,
                },
                "account_id": {
                    "type": "integer",
                    "description": "The account ID of the author.",
                    "example": 123,
                },
                "title": {
                    "type": "string",
                    "description": "The title of the post.",
                    "example": "Hello World",
                },
                "source": {
                    "type": "string",
                    "description": "The source of the post.",
                    "example": "https://www.google.com",
                },
                "score": {
                    "type": "integer",
                    "description": "The score of the post.",
                    "example": 123,
                },
                "content": {
                    "type": "string",
                    "description": "The content of the post.",
                    "example": "Hello World",
                },
                "created_at": {
                    "type": "string",
                    "description": "The creation time of the post.",
                    "example": "2020-01-01 00:00:00",
                },
                "image_preview_url": {
                    "type": "string",
                    "description": "The preview URL of the image.",
                    "example": "/api/images/12345678-1234-5678-1234-567812345678.jpg",
                }
            }
        }
    }
}

@bp.route("/posts", methods=["GET"])
@swag_from(specs_dict)
def get_posts():
    """Get posts.

    This endpoint allows users to retrieve posts.

    ---
    tags:
        - posts
    parameters:
        - in: query
          name: page
          type: integer
          description: Page number.
          default: 1
        - in: query
          name: per_page
          type: integer
          description: Number of posts per page.
          default: 10
    responses:
        200:
            description: Posts retrieved successfully.
            schema:
                type: array
                items:
                    $ref: '#/definitions/Post'
        400:
            description: Invalid parameters.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error message.
                        example: invalid parameters
    """
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return jsonify({"message": "invalid parameters"}), 400

    # post join image
    posts = Post.query.order_by(Post.created_at.desc()).join(Image).paginate(page=page, per_page=per_page, error_out=False).items
    res = []
    for post in posts:
        res.append(post.to_dict())
        res[-1]["image_preview_url"] = post.images[0].preview_url

    return jsonify(res), 200