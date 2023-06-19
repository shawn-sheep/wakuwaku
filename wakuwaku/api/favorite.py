from flask import request, jsonify
from wakuwaku.api import bp
from wakuwaku.models import Post, db, Favorite, Account
from flask_login import login_required, current_user

@bp.route("/favorite", methods=["POST"])
@login_required
def favorite():
    """
    Favorite a post.

    ---
    tags:
      - Favorites
    parameters:
        -   name: post_id
            in: formData
            type: integer
            required: true
            description: The ID of the post to favorite.
        -   name: favorite
            in: formData
            type: string
            enum: ['favorite', 'unfavorite']
            required: true
            description: The type of favorite ('favorite' or 'unfavorite').
    responses:
        200:
            description: The favorite was recorded successfully.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Success message.
                example: Favorite recorded
                fav_count:
                type: integer
                description: The current favorite count for the post.
                example: 15
        400:
            description: Failed to record the favorite.
            schema:
            type: object
            properties:
                message:
                    type: string
                    description: Error message.
                    example: Favorite failed
        404:
            description: The post was not found.
            schema:
            type: object
            properties:
                message:
                    type: string
                    description: Error message.
                    example: Post not found
    """
    try:
        post_id = request.form.get("post_id")
        favorite_type = request.form.get("favorite")
    except ValueError:
        return jsonify({"message": "Invalid request"}), 400

    account_id = current_user.account_id

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404
    
    if favorite_type not in ['favorite', 'unfavorite']:
        return jsonify({"message": "Invalid favorite type"}), 400

    favorite = Favorite.query.filter_by(post_id=post_id, account_id=account_id).first()
    if favorite_type == 'favorite':
        if favorite:
            return jsonify({"message": "Already favorited"}), 400
        else:
            favorite = Favorite(post_id=post_id, account_id=account_id)
            db.session.add(favorite)
            post.fav_count += 1
            db.session.commit()
            return jsonify({"message": "Favorite recorded", "fav_count": post.fav_count}), 200
    elif favorite_type == 'unfavorite':
        if not favorite:
            return jsonify({"message": "Not favorited"}), 400
        else:
            db.session.delete(favorite)
            post.fav_count -= 1
            db.session.commit()
            return jsonify({"message": "Unfavorited", "fav_count": post.fav_count}), 200