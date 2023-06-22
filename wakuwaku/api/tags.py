from wakuwaku.api import bp
from wakuwaku.models import Tag
from wakuwaku.extensions import db, cache

from flask import request, jsonify

@bp.route("/autocomplete", methods=["GET"])
def autocomplete():
    """Autocomplete tags.

    This endpoint allows users to autocomplete tags.
    
    ---
    tags:
        - tags
    parameters:
        -   name: q
            in: query
            type: string
            required: true
            description: The query string.
    responses:
        200:
            description: Tags found.
            schema:
                type: object
                properties:
                    tags:
                        type: array
                        items:
                            $ref: "#/definitions/Tag"
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
        q = request.args.get("q")
    except KeyError:
        return jsonify({"message": "invalid parameters"}), 400
    
    # 按照tag.count排序，最多返回10个tag
    tags = Tag.query.filter(Tag.name.like(f"%{q}%")).order_by(Tag.count.desc()).limit(10).all()
    tags = [tag.to_dict() for tag in tags]
    return jsonify({"tags": tags}), 200

from sqlalchemy import text

@bp.route("/tags", methods=["GET"])
@cache.cached(timeout=3600, query_string=True)
def get_tags():
    """Get top tags for the homepage.

    This endpoint allows users to retrieve top tags for the homepage arranged by tag.type.
    
    ---
    tags:
        - tags
    parameters:
        -   name: count
            in: query
            type: integer
            required: false
            description: The number of tags per type.
    responses:
        200:
            description: Tags found.
            schema:
                type: array
                items:
                    $ref: "#/definitions/Tag"
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
        count = int(request.args.get("count", 10))
    except (TypeError, ValueError):
        return jsonify({"message": "invalid parameters"}), 400
    query = text('''
        WITH ranked_tags AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY type ORDER BY count DESC) AS rank
            FROM tag
        )
        SELECT tag_id, type, name, count
        FROM ranked_tags
        WHERE rank <= :count
    '''
    ).params(count=count)
    tags = db.engine.execute(query).fetchall()
    tags = [dict(tag) for tag in tags]
    return jsonify(tags), 200