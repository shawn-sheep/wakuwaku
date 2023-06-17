from flask import request, jsonify
from wakuwaku.api import bp
from wakuwaku.models import Post, db, Vote, Account
from flask_login import login_required, current_user

@bp.route("/vote", methods=["POST"])
@login_required
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
        enum: ['up', 'down', 'cancel']
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
            score:
              type: integer
              description: The current score for the post.
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
    account_id = current_user.account_id

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404
    
    if vote_type not in ['up', 'down', 'cancel']:
        return jsonify({"message": "Invalid vote type"}), 400
    
    vote = Vote.query.filter_by(account_id=account_id, post_id=post_id).first()
    
    if vote_type == 'cancel':
        if not vote:
            return jsonify({"message": "Vote not found"}), 404
        else:
            db.session.delete(vote)
            post.score -= vote.value
            db.session.commit()
            return jsonify({
                "message": "Vote cancelled",
                "score": post.score
            }), 200
        
    pre_value = vote.value if vote else 0
    new_value = 1 if vote_type == 'up' else -1

    if pre_value == new_value:
        return jsonify({"message": "Vote already recorded"}), 400
    
    if vote:
        vote.value = new_value
    else:
        vote = Vote(account_id=account_id, post_id=post_id, value=new_value)
        db.session.add(vote)

    post.score += new_value - pre_value

    db.session.commit()

    return jsonify({
        "message": "Vote recorded",
        "score": post.score
    }), 200