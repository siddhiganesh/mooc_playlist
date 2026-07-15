from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Assignment, AssignmentSubmission, Course, Enrollment
from datetime import datetime

assignments_bp = Blueprint("assignments", __name__)


@assignments_bp.route("", methods=["GET"])
@jwt_required()
def list_assignments():
    user_id = int(get_jwt_identity())
    enrolled_ids = [e.course_id for e in Enrollment.query.filter_by(user_id=user_id).all()]
    if not enrolled_ids:
        return jsonify({"assignments": []})
    assignments = Assignment.query.filter(Assignment.course_id.in_(enrolled_ids)).all()
    result = []
    for a in assignments:
        sub = AssignmentSubmission.query.filter_by(assignment_id=a.id, user_id=user_id).first()
        result.append(
            {
                "id": a.id,
                "title": a.title,
                "description": a.description,
                "course_id": a.course_id,
                "course_title": a.course.title,
                "due_date": a.due_date.isoformat() if a.due_date else None,
                "total_marks": a.total_marks,
                "submitted": sub is not None,
                "grade": sub.grade if sub else None,
            }
        )
    return jsonify({"assignments": result})


@assignments_bp.route("/<int:assignment_id>", methods=["GET"])
@jwt_required()
def get_assignment(assignment_id):
    a = Assignment.query.get_or_404(assignment_id)
    user_id = int(get_jwt_identity())
    sub = AssignmentSubmission.query.filter_by(assignment_id=a.id, user_id=user_id).first()
    return jsonify(
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "course_id": a.course_id,
            "course_title": a.course.title,
            "due_date": a.due_date.isoformat() if a.due_date else None,
            "total_marks": a.total_marks,
            "submission": {
                "content": sub.content,
                "grade": sub.grade,
                "feedback": sub.feedback,
                "submitted_at": sub.submitted_at.isoformat(),
            }
            if sub
            else None,
        }
    )


@assignments_bp.route("/<int:assignment_id>/submit", methods=["POST"])
@jwt_required()
def submit(assignment_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    assignment = Assignment.query.get_or_404(assignment_id)
    existing = AssignmentSubmission.query.filter_by(
        assignment_id=assignment_id, user_id=user_id
    ).first()
    if existing:
        existing.content = data.get("content", existing.content)
        existing.file_url = data.get("file_url", existing.file_url)
        existing.submitted_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Submission updated", "id": existing.id})

    sub = AssignmentSubmission(
        assignment_id=assignment_id,
        user_id=user_id,
        content=data.get("content", ""),
        file_url=data.get("file_url", ""),
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "Submitted", "id": sub.id}), 201
