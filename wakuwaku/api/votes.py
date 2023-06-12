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
    account_id = request.form.get("account_id")
    vote_type = request.form.get("vote")

    post = Post.query.get(post_id)
    user = Account.query.get(account_id)
    if not post or not user:
        return jsonify({"message": "Post or user not found"}), 404

    vote = Vote.query.filter_by(account_id=account_id, post_id=post_id).first()
    if(vote):
        if(vote_type == 'cancel'):
            db.session.delete(vote)
            post.votes -= vote.value
        else:
            return jsonify({"message": "Vote already recorded"}), 400
    else:
        if(vote_type == 'up'):
            vote = Vote(account_id=account_id, post_id=post_id, value=1)
            post.votes += 1
        elif(vote_type == 'down'):
            vote = Vote(account_id=account_id, post_id=post_id, value=-1)
            post.votes -= 1
        else:
            return jsonify({"message": "Invalid vote type"}), 400

        db.session.add(vote)

    db.session.commit()

    return jsonify({
        "message": "Vote recorded",
        "votes": post.votes
    }), 200
