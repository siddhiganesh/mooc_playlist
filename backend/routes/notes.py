from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Note, Video

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("", methods=["GET"])
@jwt_required()
def list_notes():
    user_id = int(get_jwt_identity())
    video_id = request.args.get("video_id", type=int)
    query = Note.query.filter_by(user_id=user_id)
    if video_id:
        query = query.filter_by(video_id=video_id)
    notes = query.order_by(Note.timestamp).all()
    return jsonify(
        {
            "notes": [
                {
                    "id": n.id,
                    "video_id": n.video_id,
                    "video_title": n.video.title,
                    "content": n.content,
                    "timestamp": n.timestamp,
                    "created_at": n.created_at.isoformat(),
                }
                for n in notes
            ]
        }
    )


@notes_bp.route("", methods=["POST"])
@jwt_required()
def create_note():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    if not data.get("content") or not data.get("video_id"):
        return jsonify({"error": "content and video_id required"}), 400
    video = Video.query.get(data["video_id"])
    if not video:
        return jsonify({"error": "Video not found"}), 404
    note = Note(
        user_id=user_id,
        video_id=data["video_id"],
        content=data["content"],
        timestamp=float(data.get("timestamp", 0)),
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(
        {
            "id": note.id,
            "video_id": note.video_id,
            "content": note.content,
            "timestamp": note.timestamp,
            "created_at": note.created_at.isoformat(),
        }
    ), 201


@notes_bp.route("/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    user_id = int(get_jwt_identity())
    note = Note.query.get_or_404(note_id)
    if note.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json() or {}
    note.content = data.get("content", note.content)
    note.timestamp = float(data.get("timestamp", note.timestamp))
    db.session.commit()
    return jsonify({"message": "Updated"})


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = int(get_jwt_identity())
    note = Note.query.get_or_404(note_id)
    if note.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Deleted"})
