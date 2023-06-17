from wakuwaku.api import bp
from wakuwaku.models import Account, Post, Comment, Vote, Image, PostTag, Tag
from wakuwaku.extensions import db, swagger

from flasgger import swag_from

from flask import request, jsonify, current_app
from flask_login import login_required, current_user

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
                },
                "tags": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Tag"
                    }
                },
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
                "width": {
                    "type": "integer",
                    "description": "The width of the image.",
                    "example": 123,
                },
                "height": {
                    "type": "integer",
                    "description": "The height of the image.",
                    "example": 123,
                },
            }
        },
        "Tag": {
            "type": "object",
            "properties": {
                "tag_id": {
                    "type": "integer",
                    "description": "The tag ID.",
                    "example": 123,
                },
                "type": {
                    "type": "integer",
                    "description": "The type of the tag.",
                    "example": 0,
                },
                "name": {
                    "type": "string",
                    "description": "The name of the tag.",
                    "example": "abc",
                },
                "count": {
                    "type": "integer",
                    "description": "The count of the tag.",
                    "example": 123,
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
          enum: ["new", "old", "score", "rank"]
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
        504:
            description: Timeout.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error message.
                        example: query timeout (1000ms)
    """
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            raise ValueError
        per_page = int(request.args.get("per_page", 10))
        if per_page < 1:
            raise ValueError
        tags = request.args.get("tags", "")
        order = request.args.get("order", "new")
        if order not in ["new", "old", "score", "rank"]:
            raise ValueError
    except ValueError:
        return jsonify({"message": "invalid parameters"}), 400

    tag_query = db.session.query(Tag).filter(Tag.name.in_(tags.split()))
    tags_info = tag_query.all()

    if len(tags_info) != len(tags.split()):
        unknown_tags = [tag for tag in tags.split() if tag not in [tag.name for tag in tags_info]]
        return jsonify({"message": "tags not found", "unknown_tags": unknown_tags}), 201

    post_query = db.session.query(Post, Image.preview_url, Image.width, Image.height).outerjoin(Post.images)
    for tag in tags_info:
        post_query = post_query.filter(Post.post_tags.any(tag_id=tag.tag_id))

    order_dict = {
        "new": Post.created_at.desc(),
        "old": Post.created_at.asc(),
        "score": Post.score.desc(),
        "rank": Post.score.desc(),
    }

    if order == "rank":
        # 最近一周的热度
        from datetime import datetime, timedelta
        post_query = post_query.filter(Post.created_at > datetime.now() - timedelta(days=30))

    post_query = post_query.order_by(order_dict[order])
    post_query = post_query.limit(per_page).offset((page - 1) * per_page)
    # 设置超时
    db.session.execute("SET SESSION STATEMENT_TIMEOUT TO 1000")

    from sqlalchemy.exc import OperationalError

    posts = {}
    try:
        for post, preview_url, width, height in post_query.all():
            if post.post_id not in posts:
                posts[post.post_id] = post.to_dict()
                posts[post.post_id].update({"preview_url": preview_url, "width": width, "height": height})
    except OperationalError as e:
        if "canceling statement due to statement timeout" in str(e):
            return jsonify({"message": "query timeout (1000ms)"}), 504
        else:
            raise e


    res = [post for post in posts.values()]


    return jsonify(res), 200

@bp.route("/posts/<int:post_id>", methods=["GET"])
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
    post = Post.query.get(post_id)
    if post is None:
        return jsonify({"message": "post not found"}), 404
    res = post.to_dict()
    res["images"] = []
    for image in post.images:
        res["images"].append(image.to_dict())

    tags_query = db.session.query(Tag).join(PostTag).filter(PostTag.post_id == post_id)

    res["tags"] = [tag.to_dict() for tag in tags_query.all()]
        
    return jsonify(res), 200

@bp.route("/posts", methods=["POST"])
@login_required
def create_post():
    """Create a post.

    This endpoint allows users to create a post.

    ---
    tags:
        - posts
    parameters:
        -   name: title
            in: formData
            type: string
            description: The title of the post.
        -   name: content
            in: formData
            type: string
            description: The content of the post.
        -   name: source
            in: formData
            type: string
            required: true
            description: The source of the post.
        -   name: tags
            in: formData
            type: string
            description: The tags of the post separated by space.
        -   name: images
            in: formData
            type: file
            description: The images of the post.
    responses:
        201:
            description: Post created successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Success message.
                        example: post created successfully
                    post_id:
                        type: integer
                        description: ID of the post.
                        example: 1
        400:
            description: Invalid parameters.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error message.
                        example: invalid parameters
        422:
            description: Invalid parameters.
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
                        example: ["tag1", "tag2"]
    """
    try:
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        source = request.form["source"]
        tags = request.form.get("tags", "").split()
        images = request.files.getlist("images")
    except KeyError:
        return jsonify({"message": "invalid parameters"}), 400

    from sqlalchemy import insert

    insert_post = insert(Post).values(
        account_id=current_user.account_id,
        title=title,
        content=content,
        source=source,
        score=0,
    ).returning(Post.post_id)

    # 添加 tags
    insert_tags = []
    if tags:
        tag_query = db.session.query(Tag).filter(Tag.name.in_(tags))
        tags_info = tag_query.all()

        if len(tags_info) != len(tags):
            unknown_tags = [tag for tag in tags if tag not in [tag.name for tag in tags_info]]
            return jsonify({"message": "tags not found", "unknown_tags": unknown_tags}), 422

        insert_tags = [{"tag_id": tag.tag_id} for tag in tags_info]

    # 添加 images
    insert_images = []
    from wakuwaku.utils import save_file
    from PIL import Image as PILImage
    for image in images:
        # 把image转为PILImage
        original_image = PILImage.open(image)
        sample_image = original_image.copy()
        sample_image.thumbnail((720, 720))
        preview_image = original_image.copy()
        preview_image.thumbnail((180, 180))

        # 保存原图
        original_url = save_file(original_image, "original", 100)
        # 保存预览图
        preview_url = save_file(preview_image, "preview")
        # 保存缩略图
        sample_url = save_file(sample_image, "sample")

        # 添加到数据库
        insert_images.append({
            "name": image.filename.split(".")[0][:255],
            "original_url": original_url,
            "preview_url": preview_url,
            "sample_url": sample_url,
            "width": original_image.width,
            "height": original_image.height,
        })

    post_id = db.session.execute(insert_post).fetchone()[0]

    for tag in insert_tags:
        db.session.add(PostTag(
            post_id=post_id,
            tag_id=tag["tag_id"],
        ))

    for image in insert_images:
        db.session.add(Image(
            post_id=post_id,
            name=image["name"],
            original_url=image["original_url"],
            preview_url=image["preview_url"],
            sample_url=image["sample_url"],
            width=image["width"],
            height=image["height"],
        ))

    db.session.commit()

    return jsonify({
        "message": "post created successfully",
        "post_id": post_id}), 201