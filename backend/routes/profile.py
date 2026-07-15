from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, bcrypt
from models import User, Enrollment, Certificate, QuizAttempt
from sqlalchemy import func

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "bio": user.bio,
            "avatar": user.avatar,
            "role": user.role,
            "points": user.points,
            "created_at": user.created_at.isoformat(),
            "stats": {
                "courses_enrolled": Enrollment.query.filter_by(user_id=user_id).count(),
                "certificates": Certificate.query.filter_by(user_id=user_id).count(),
                "quizzes_attempted": QuizAttempt.query.filter_by(user_id=user_id).count(),
            },
        }
    )


@profile_bp.route("", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    user.full_name = data.get("full_name", user.full_name)
    user.bio = data.get("bio", user.bio)
    user.avatar = data.get("avatar", user.avatar)
    db.session.commit()
    return jsonify({"message": "Profile updated"})


@profile_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    if not data.get("old_password") or not data.get("new_password"):
        return jsonify({"error": "old_password and new_password required"}), 400
    if not bcrypt.check_password_hash(user.password_hash, data["old_password"]):
        return jsonify({"error": "Old password incorrect"}), 400
    user.password_hash = bcrypt.generate_password_hash(data["new_password"]).decode("utf-8")
    db.session.commit()
    return jsonify({"message": "Password updated"})


@profile_bp.route("/stats", methods=["GET"])
@jwt_required()
def stats():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    avg_progress = (
        sum([e.progress for e in enrollments]) / len(enrollments) if enrollments else 0
    )
    certs = Certificate.query.filter_by(user_id=user_id).count()
    attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    avg_score = sum([a.score for a in attempts]) / len(attempts) if attempts else 0
    return jsonify(
        {
            "avg_progress": round(avg_progress, 2),
            "certificates": certs,
            "avg_quiz_score": round(avg_score, 2),
            "total_points": user.points,
        }
    )
