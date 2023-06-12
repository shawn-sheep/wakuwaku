from flask import request, jsonify
from wakuwaku.api import bp
from wakuwaku.models import Post, db, Vote, Account

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
      - name: user_id
        in: formData
        type: integer
        required: true
        description: The ID of the user casting the vote.
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
    user_id = request.form.get("user_id")
    vote_type = request.form.get("vote")

    post = Post.query.get(post_id)
    user = Account.query.get(user_id)
    if not post or not user:
        return jsonify({"message": "Post or user not found"}), 404

    vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
    if vote:
        return jsonify({"message": "You have already voted on this post"}), 400

    vote = Vote(user_id=user_id, post_id=post_id, vote=vote_type)
    db.session.add(vote)

    if vote_type == "up":
        post.votes += 1
    elif vote_type == "down":
        post.votes -= 1

    db.session.commit()

    return jsonify({
        "message": "Vote recorded",
        "votes": post.votes
    }), 200
