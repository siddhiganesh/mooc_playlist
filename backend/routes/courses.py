from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Course, Video, Enrollment

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("", methods=["GET"])
@jwt_required()
def list_courses():
    user_id = int(get_jwt_identity())
    category = request.args.get("category")
    search = request.args.get("search")

    query = Course.query
    if category and category != "All":
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Course.title.ilike(f"%{search}%"))

    courses = query.all()
    enrolled_ids = {e.course_id for e in Enrollment.query.filter_by(user_id=user_id).all()}

    return jsonify(
        {
            "courses": [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "instructor": c.instructor,
                    "category": c.category,
                    "difficulty": c.difficulty,
                    "thumbnail": c.thumbnail,
                    "duration_hours": c.duration_hours,
                    "rating": c.rating,
                    "students_count": c.students_count,
                    "enrolled": c.id in enrolled_ids,
                    "video_count": len(c.videos),
                }
                for c in courses
            ]
        }
    )


@courses_bp.route("/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    user_id = int(get_jwt_identity())
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    return jsonify(
        {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "instructor": course.instructor,
            "category": course.category,
            "difficulty": course.difficulty,
            "thumbnail": course.thumbnail,
            "duration_hours": course.duration_hours,
            "rating": course.rating,
            "students_count": course.students_count,
            "enrolled": enrollment is not None,
            "progress": enrollment.progress if enrollment else 0.0,
            "videos": [
                {
                    "id": v.id,
                    "title": v.title,
                    "description": v.description,
                    "url": v.url,
                    "duration": v.duration,
                    "order": v.order,
                    "thumbnail": v.thumbnail,
                }
                for v in sorted(course.videos, key=lambda x: x.order)
            ],
        }
    )


@courses_bp.route("/<int:course_id>/enroll", methods=["POST"])
@jwt_required()
def enroll(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.get_or_404(course_id)
    existing = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return jsonify({"message": "Already enrolled", "progress": existing.progress})

    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    course.students_count += 1
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrolled successfully", "progress": 0.0}), 201


@courses_bp.route("/<int:course_id>/progress", methods=["PUT"])
@jwt_required()
def update_progress(course_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not enrollment:
        return jsonify({"error": "Not enrolled"}), 404
    enrollment.progress = float(data.get("progress", enrollment.progress))
    from datetime import datetime
    enrollment.last_accessed = datetime.utcnow()
    db.session.commit()
    return jsonify({"progress": enrollment.progress})


@courses_bp.route("/my", methods=["GET"])
@jwt_required()
def my_courses():
    user_id = int(get_jwt_identity())
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    return jsonify(
        {
            "courses": [
                {
                    "id": e.course.id,
                    "title": e.course.title,
                    "description": e.course.description,
                    "instructor": e.course.instructor,
                    "category": e.course.category,
                    "difficulty": e.course.difficulty,
                    "thumbnail": e.course.thumbnail,
                    "duration_hours": e.course.duration_hours,
                    "rating": e.course.rating,
                    "progress": e.progress,
                    "enrolled_at": e.enrolled_at.isoformat(),
                    "last_accessed": e.last_accessed.isoformat(),
                }
                for e in enrollments
            ]
        }
    )
