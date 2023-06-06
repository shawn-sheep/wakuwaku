from wakuwaku.api import bp
from wakuwaku.models import Account, Post, Comment, Vote, Image, PostTag, Tag
from wakuwaku.extensions import db, swagger

from sqlalchemy.orm import joinedload

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
                }
            }
        },
        "PostPreview": {
            "type": "object",
            "properties": {
                "image_preview_url": {
                    "type": "string",
                    "description": "The preview URL of the image.",
                    "example": "/api/images/12345678-1234-5678-1234-567812345678.jpg",
                }
            }
        },
        "PostDetail": {
            "type": "object",
            "properties": {
                "images": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Image"
                    }
                }
            }
        },
        "Image": {
            "type": "object",
            "properties": {
                "image_id": {
                    "type": "integer",
                    "description": "The image ID.",
                    "example": 123,
                },
                "post_id": {
                    "type": "integer",
                    "description": "The post ID of the image.",
                    "example": 123,
                },
                "name": {
                    "type": "string",
                    "description": "The name of the image.",
                    "example": "abc",
                },
                "preview_url": {
                    "type": "string",
                    "description": "The preview URL of the image.",
                    "example": "/api/images/12345678-1234-5678-1234-567812345678.jpg",
                },
                "sample_url": {
                    "type": "string",
                    "description": "The sample URL of the image.",
                    "example": "/api/images/12345678-1234-5678-1234-567812345678.jpg",
                },
                "original_url": {
                    "type": "string",
                    "description": "The original URL of the image.",
                    "example": "/api/images/12345678-1234-5678-1234-567812345678.jpg",
                },
            }
        }
    }
}

specs_dict["definitions"]["PostPreview"]["properties"] = {**specs_dict["definitions"]["Post"]["properties"], **specs_dict["definitions"]["PostPreview"]["properties"]}
specs_dict["definitions"]["PostDetail"]["properties"] = {**specs_dict["definitions"]["Post"]["properties"], **specs_dict["definitions"]["PostDetail"]["properties"]}

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
        - in: query
          name: tags
          type: string
          description: Tags of the posts separated by space.
          default: ""
        - in: query
          name: order
          type: string
          description: Order of the posts.
          default: "new"
          enum: ["new", "old", "score"] 
    responses:
        200:
            description: Posts retrieved successfully.
            schema:
                type: array
                items:
                    $ref: '#/definitions/PostPreview'
        201:
            description: tags not found.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error message.
                        example: tags not found
                    unknown_tags:
                        type: array
                        items:
                            type: string
                        description: Unknown tags.
                        example: ["abc"]
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
        tags = request.args.get("tags", "")
        order = request.args.get("order", "new")
    except ValueError:
        return jsonify({"message": "invalid parameters"}), 400

    tag_query = db.session.query(Tag).filter(Tag.name.in_(tags.split()))
    tags_info = tag_query.all()

    if len(tags_info) != len(tags.split()):
        unknown_tags = [tag for tag in tags.split() if tag not in [tag.name for tag in tags_info]]
        return jsonify({"message": "tags not found", "unknown_tags": unknown_tags}), 201

    post_query = db.session.query(Post, Image.preview_url).outerjoin(Post.images)
    for tag in tags_info:
        post_query = post_query.filter(Post.post_tags.any(tag_id=tag.tag_id))

    order_dict = {
        "new": Post.created_at.desc(),
        "old": Post.created_at.asc(),
        "score": Post.score.desc(),
    }

    post_query = post_query.order_by(order_dict[order])

    post_query = post_query.limit(per_page).offset((page - 1) * per_page)

    # post_join_image = db.session.query(Post, Image.preview_url).join(Post.images).filter(Post.post_id.in_(post_query))

    # post_join_image = post_join_image.order_by(order_dict[order])

    # print(post_query.statement)

    posts = {}
    for post, preview_url in post_query.all():
        if post.post_id not in posts:
            posts[post.post_id] = post.to_dict()
        if preview_url is not None:
            posts[post.post_id]["preview_url"] = preview_url
        else:
            posts[post.post_id]["preview_url"] = ""

    res = [post for post in posts.values()]


    return jsonify(res), 200

@bp.route("/posts/<int:post_id>", methods=["GET"])
@swag_from(specs_dict)
def get_post(post_id):
    """Get a post.

    This endpoint allows users to retrieve a post by ID.

    ---
    tags:
        - posts
    parameters:
        - name: post_id
          in: path
          type: integer
          required: true
          description: The ID of the post.
    responses:
        200:
            description: Post retrieved successfully.
            schema:
                $ref: '#/definitions/PostDetail'
        404:
            description: Post not found.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error message.
                        example: post not found
    """
    from sqlalchemy import select
    post_images_query = select(Post, Image).join_from(Post, Image).where(Post.post_id == post_id)

    # images 添加到 images 字段
    post_images = db.session.execute(post_images_query).all()
    if len(post_images) == 0:
        return jsonify({"message": "post not found"}), 404
    res = post_images[0][0].to_dict()
    res["images"] = []
    for post, image in post_images:
        res["images"].append(image.to_dict())

    return jsonify(res), 200