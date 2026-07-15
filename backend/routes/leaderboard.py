from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Enrollment, Certificate
from extensions import db
from sqlalchemy import func

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("", methods=["GET"])
@jwt_required()
def leaderboard():
    current_user_id = int(get_jwt_identity())
    users = User.query.order_by(User.points.desc()).limit(50).all()

    result = []
    for idx, u in enumerate(users, start=1):
        cert_count = Certificate.query.filter_by(user_id=u.id).count()
        course_count = Enrollment.query.filter_by(user_id=u.id).count()
        result.append(
            {
                "rank": idx,
                "id": u.id,
                "username": u.username,
                "full_name": u.full_name,
                "avatar": u.avatar,
                "points": u.points,
                "certificates": cert_count,
                "courses_completed": course_count,
                "is_you": u.id == current_user_id,
            }
        )
    return jsonify({"leaderboard": result})
