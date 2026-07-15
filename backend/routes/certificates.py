import uuid
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Certificate, Enrollment, Course, User

certificates_bp = Blueprint("certificates", __name__)


@certificates_bp.route("", methods=["GET"])
@jwt_required()
def list_certificates():
    user_id = int(get_jwt_identity())
    certs = Certificate.query.filter_by(user_id=user_id).all()
    return jsonify(
        {
            "certificates": [
                {
                    "id": c.id,
                    "course_id": c.course_id,
                    "course_title": c.course.title,
                    "instructor": c.course.instructor,
                    "issued_at": c.issued_at.isoformat(),
                    "certificate_code": c.certificate_code,
                }
                for c in certs
            ]
        }
    )


@certificates_bp.route("/generate/<int:course_id>", methods=["POST"])
@jwt_required()
def generate(course_id):
    user_id = int(get_jwt_identity())
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if not enrollment:
        return jsonify({"error": "Not enrolled in this course"}), 400
    if enrollment.progress < 100:
        return jsonify({"error": "Complete the course to earn certificate"}), 400

    existing = Certificate.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return jsonify(
            {
                "certificate_code": existing.certificate_code,
                "issued_at": existing.issued_at.isoformat(),
                "course_title": existing.course.title,
                "instructor": existing.course.instructor,
            }
        )

    code = "CERT-" + uuid.uuid4().hex[:10].upper()
    cert = Certificate(
        user_id=user_id,
        course_id=course_id,
        certificate_code=code,
    )
    db.session.add(cert)

    user = User.query.get(user_id)
    user.points = (user.points or 0) + 500
    db.session.commit()

    return jsonify(
        {
            "certificate_code": code,
            "issued_at": cert.issued_at.isoformat(),
            "course_title": cert.course.title,
            "instructor": cert.course.instructor,
        }
    ), 201


@certificates_bp.route("/verify/<string:code>", methods=["GET"])
def verify(code):
    cert = Certificate.query.filter_by(certificate_code=code).first()
    if not cert:
        return jsonify({"valid": False}), 404
    return jsonify(
        {
            "valid": True,
            "user": cert.user.full_name or cert.user.username,
            "course": cert.course.title,
            "issued_at": cert.issued_at.isoformat(),
        }
    )
