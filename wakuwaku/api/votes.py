from flask import request, jsonify
from wakuwaku.api import bp
from wakuwaku.models import Post, db

@bp.route("/vote", methods=["POST"])
def vote():
    """
    Vote on a post.

    ---
    tags:
      - Voting
    parameters:
      - name: post_id
        in: formData
        type: integer
        required: true
        description: The ID of the post to vote on.
      - name: vote
        in: formData
        type: string
        enum: ['up', 'down']
        required: true
        description: The type of vote ('up' or 'down').
    responses:
      200:
        description: The vote was recorded successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message.
              example: Vote recorded
            votes:
              type: integer
              description: The current vote count for the post.
              example: 15
      400:
        description: Failed to record the vote.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message.
              example: Vote failed
    """
    post_id = request.form.get("post_id")
    vote_type = request.form.get("vote")

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404

    if vote_type == "up":
        post.votes += 1
    elif vote_type == "down":
        post.votes -= 1
    else:
        return jsonify({"message": "Invalid vote type"}), 400

    db.session.commit()

    return jsonify({
        "message": "Vote recorded",
        "votes": post.votes
    }), 200
