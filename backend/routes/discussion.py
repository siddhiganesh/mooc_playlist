from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Discussion, User, Course
from datetime import datetime

discussion_bp = Blueprint("discussion", __name__)


def _serialize(d):
    return {
        "id": d.id,
        "user_id": d.user_id,
        "username": d.user.username,
        "full_name": d.user.full_name,
        "avatar": d.user.avatar,
        "course_id": d.course_id,
        "course_title": d.course.title if d.course else None,
        "parent_id": d.parent_id,
        "content": d.content,
        "likes": d.likes,
        "created_at": d.created_at.isoformat(),
        "reply_count": len(d.replies),
    }


@discussion_bp.route("", methods=["GET"])
@jwt_required()
def list_posts():
    course_id = request.args.get("course_id", type=int)
    query = Discussion.query.filter(Discussion.parent_id.is_(None))
    if course_id:
        query = query.filter_by(course_id=course_id)
    posts = query.order_by(Discussion.created_at.desc()).all()
    return jsonify({"posts": [_serialize(p) for p in posts]})


@discussion_bp.route("/<int:post_id>", methods=["GET"])
@jwt_required()
def get_post(post_id):
    post = Discussion.query.get_or_404(post_id)
    replies = [_serialize(r) for r in sorted(post.replies, key=lambda x: x.created_at)]
    return jsonify({"post": _serialize(post), "replies": replies})


@discussion_bp.route("", methods=["POST"])
@jwt_required()
def create_post():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    if not data.get("content"):
        return jsonify({"error": "content required"}), 400
    post = Discussion(
        user_id=user_id,
        course_id=data.get("course_id"),
        parent_id=data.get("parent_id"),
        content=data["content"],
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(_serialize(post)), 201


@discussion_bp.route("/<int:post_id>/like", methods=["POST"])
@jwt_required()
def like_post(post_id):
    post = Discussion.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify({"likes": post.likes})


@discussion_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())
    post = Discussion.query.get_or_404(post_id)
    if post.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    for reply in post.replies:
        db.session.delete(reply)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Deleted"})
