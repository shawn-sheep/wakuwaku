from wakuwaku.api import bp
from wakuwaku.models import Account, Post, Comment, Vote, Image, PostTag, Tag, Favorite
from wakuwaku.extensions import db

from flasgger import swag_from

from flask import request, jsonify
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
                "fav_count": {
                    "type": "integer",
                    "description": "The favorite count of the post.",
                    "example": 123,
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
                    "example": "Wed, 01 Jan 2020 00:00:00 GMT",
                },
                "rating": {
                    "type": "string",
                    "description": "The rating of the post.",
                    "enum": ["g", "s", "q", "e"],
                    "example": "g",
                },
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
                "self_vote": {
                    "type": "integer",
                    "description": "The vote of the current user.",
                    "example": 1,
                },
                "self_fav": {
                    "type": "boolean",
                    "description": "The favorite of the current user.",
                    "example": True,
                },
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
                "image_count": {
                    "type": "integer",
                    "description": "The number of images in the post.",
                    "example": 1,
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

from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError
from sqlalchemy import func, and_, text

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
          name: offset
          type: integer
          description: The offset of the posts.
          default: 0
        - in: query
          name: before_id
          type: integer
          description: The ID of the post before which the posts are retrieved. (set to 0 to ignore)
          default: 0
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
          name: uploader_id
          type: integer
          description: The ID of the uploader.
        - in: query
          name: favorited_by
          type: integer
          description: The ID of the user who favorited the posts.
        - in: query
          name: ratings
          type: string
          description: The ratings of the posts separated by space. (g, s, q, e)
          default: "g"
        - in: query
          name: order
          type: string
          description: Order of the posts.
          default: "new"
          enum: ["new", "old", "score", "rank", "random"]
        - in: query
          name: quality
          type: string
          description: Quality of the images.
          default: "preview"
          enum: ["preview", "sample", "original"]
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
        offset = int(request.args.get("offset", 0))
        if offset < 0:
            raise ValueError
        before_id = int(request.args.get("before_id", 0))
        per_page = int(request.args.get("per_page", 10))
        if per_page < 1:
            raise ValueError
        tags = request.args.get("tags", "")
        uploader_id = int(request.args.get("uploader_id", 0))
        favorited_by = int(request.args.get("favorited_by", 0))
        ratings = request.args.get("ratings", "g")
        for rating in ratings.split():
            if rating not in ["g", "s", "q", "e"]:
                raise ValueError
        order = request.args.get("order", "new")
        if order not in ["new", "old", "score", "rank", "random"]:
            raise ValueError
        quality = request.args.get("quality", "preview")
        if quality not in ["preview", "sample", "original"]:
            raise ValueError
    except ValueError:
        return jsonify({"message": "invalid parameters"}), 400

    # 去重
    tags_list = list(set(tags.split()))
    tag_query = db.session.query(Tag).filter(Tag.name.in_(tags_list))
    tags_info = tag_query.all()

    # post_query = db.session.query(Post, url_dict[quality], Image.width, Image.height).outerjoin(Post.images)
    post_query = db.session.query(Post.post_id)

    if len(tags_info) != len(tags_list):
        unknown_tags = [tag for tag in tags_list if tag not in [tag.name for tag in tags_info]]
        # return jsonify({"message": "tags not found", "unknown_tags": unknown_tags}), 201
        # 未知的tag作为关键词搜索
        post_query = post_query.filter(text("to_tsvector('zhcfg', title || ' ' || content) @@ websearch_to_tsquery('zhcfg', :query)").params(query=" & ".join(unknown_tags)))

    for tag in tags_info:
        post_query = post_query.filter(Post.post_tags.any(tag_id=tag.tag_id))

    if uploader_id > 0:
        post_query = post_query.filter(Post.account_id == uploader_id)

    if favorited_by > 0:
        post_query = post_query.filter(Post.favorites.any(account_id=favorited_by))
    
    post_query = post_query.filter(Post.rating.in_(ratings.split()))

    order_dict = {
        "new": Post.post_id.desc(),
        "old": Post.post_id.asc(),
        "score": text("score desc, post.post_id desc"),
        "rank": text("score desc, post.post_id desc"),
        "random": text("random()"),
    }

    if order == "rank":
        # 最近一个月的热度
        post_query = post_query.filter(Post.created_at > datetime.now() - timedelta(days=30))

    if before_id > 0:
        post_query = post_query.filter(Post.post_id < before_id)

    post_query = post_query.order_by(order_dict[order])
    post_query = post_query.limit(per_page).offset(offset)
    # 设置超时
    db.session.execute("SET SESSION STATEMENT_TIMEOUT TO 1000")

    url_dict = {
        "preview": Image.preview_url,
        "sample": Image.sample_url,
        "original": Image.original_url,
    }

    subquery = db.session.query(Image.post_id, func.min(Image.image_id).label('min_image_id'), func.count(Image.image_id).label('image_count'))\
        .filter(Image.post_id.in_(post_query.subquery()))\
        .group_by(Image.post_id).subquery()
    post_query = db.session.query(Post, url_dict[quality], Image.width, Image.height, subquery.c.image_count)\
        .select_from(Post)\
        .join(subquery, and_(Post.post_id == subquery.c.post_id))\
        .join(Image, Image.image_id == subquery.c.min_image_id)\
        .order_by(order_dict[order])

    posts = {}
    try:
        for post, preview_url, width, height, image_count in post_query.all():
            posts[post.post_id] = post.to_dict()
            # 若url以mp4, webm, ogg结尾，降级为preview
            if preview_url.split(".")[-1] in ["mp4", "webm", "ogg"]:
                preview_url = post.images[0].preview_url
            posts[post.post_id].update({"preview_url": preview_url, "width": width, "height": height, "image_count": image_count})
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

    res["self_vote"] = 0
    if current_user.is_authenticated:
        vote = Vote.query.filter_by(account_id=current_user.account_id, post_id=post_id).first()
        if vote is not None:
            res["self_vote"] = vote.value

    res["self_fav"] = 0
    if current_user.is_authenticated:
        fav = Favorite.query.filter_by(account_id=current_user.account_id, post_id=post_id).first()
        if fav is not None:
            res["self_fav"] = 1

    res["images"] = []
    for image in post.images:
        res["images"].append(image.to_dict())

    tags_query = db.session.query(Tag).join(PostTag).filter(PostTag.post_id == post_id)

    res["tags"] = [tag.to_dict() for tag in tags_query.all()]
        
    return jsonify(res), 200

from sqlalchemy import insert
from wakuwaku.utils import save_file
from PIL import Image as PILImage

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
        -   name: rating
            in: formData
            type: string
            required: true
            description: The rating of the post.
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
        rating = request.form.get("rating", "s")
    except KeyError:
        return jsonify({"message": "invalid parameters"}), 400

    insert_post = insert(Post).values(
        account_id=current_user.account_id,
        title=title,
        content=content,
        source=source,
        score=0,
        fav_count=0,
        rating=rating,
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

from sqlalchemy import delete

@bp.route("/posts", methods=["DELETE"])
@login_required
def delete_post():
    """Delete a post.

    This endpoint allows users to delete a post.

    ---
    tags:
        - posts
    parameters:
        -   name: post_id
            in: formData
            type: integer
            required: true
            description: The ID of the post.
    responses:
        200:
            description: Post deleted successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Success message.
                        example: post deleted successfully
        404:
            description: Post not found.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error message.
                        example: post not found
        403:
            description: Permission denied.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Error message.
                        example: permission denied
    """
    try:
        post_id = int(request.form["post_id"])
    except (KeyError, ValueError):
        return jsonify({"message": "invalid parameters"}), 400

    post = Post.query.filter_by(post_id=post_id).first()
    if post is None:
        return jsonify({"message": "post not found"}), 404

    if post.account_id != current_user.account_id:
        return jsonify({"message": "permission denied"}), 403

    db.session.execute(delete(Post).where(Post.post_id == post_id))
    db.session.commit()

    return jsonify({"message": "post deleted successfully"}), 200