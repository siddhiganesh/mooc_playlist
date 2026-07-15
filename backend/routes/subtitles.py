from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Subtitle, Video

subtitles_bp = Blueprint("subtitles", __name__)


@subtitles_bp.route("/video/<int:video_id>", methods=["GET"])
@jwt_required()
def list_subtitles(video_id):
    language = request.args.get("language")
    query = Subtitle.query.filter_by(video_id=video_id)
    if language:
        query = query.filter_by(language=language)
    subtitles = query.order_by(Subtitle.start_time).all()
    return jsonify(
        {
            "subtitles": [
                {
                    "id": s.id,
                    "language": s.language,
                    "content": s.content,
                    "start_time": s.start_time,
                    "end_time": s.end_time,
                }
                for s in subtitles
            ]
        }
    )


@subtitles_bp.route("/video/<int:video_id>", methods=["POST"])
@jwt_required()
def add_subtitle(video_id):
    data = request.get_json() or {}
    if not data.get("content"):
        return jsonify({"error": "content required"}), 400
    sub = Subtitle(
        video_id=video_id,
        language=data.get("language", "en"),
        content=data["content"],
        start_time=float(data.get("start_time", 0)),
        end_time=float(data.get("end_time", 0)),
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify({"id": sub.id, "message": "Subtitle added"}), 201


@subtitles_bp.route("/<int:subtitle_id>", methods=["DELETE"])
@jwt_required()
def delete_subtitle(subtitle_id):
    sub = Subtitle.query.get_or_404(subtitle_id)
    db.session.delete(sub)
    db.session.commit()
    return jsonify({"message": "Deleted"})


@subtitles_bp.route("/video/<int:video_id>/search", methods=["GET"])
@jwt_required()
def search_subtitle(video_id):
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"subtitles": []})
    subtitles = (
        Subtitle.query.filter(Subtitle.video_id == video_id, Subtitle.content.ilike(f"%{q}%"))
        .order_by(Subtitle.start_time)
        .all()
    )
    return jsonify(
        {
            "subtitles": [
                {
                    "id": s.id,
                    "content": s.content,
                    "start_time": s.start_time,
                    "language": s.language,
                }
                for s in subtitles
            ]
        }
    )
