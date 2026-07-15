from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Playlist, PlaylistItem, Video

playlists_bp = Blueprint("playlists", __name__)


@playlists_bp.route("", methods=["GET"])
@jwt_required()
def list_playlists():
    user_id = int(get_jwt_identity())
    playlists = Playlist.query.filter_by(user_id=user_id).order_by(Playlist.created_at.desc()).all()
    return jsonify(
        {
            "playlists": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "created_at": p.created_at.isoformat(),
                    "item_count": len(p.items),
                }
                for p in playlists
            ]
        }
    )


@playlists_bp.route("", methods=["POST"])
@jwt_required()
def create_playlist():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"error": "Name required"}), 400
    playlist = Playlist(
        user_id=user_id,
        name=data["name"],
        description=data.get("description", ""),
    )
    db.session.add(playlist)
    db.session.commit()
    return jsonify(
        {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "created_at": playlist.created_at.isoformat(),
            "item_count": 0,
        }
    ), 201


@playlists_bp.route("/<int:playlist_id>", methods=["GET"])
@jwt_required()
def get_playlist(playlist_id):
    user_id = int(get_jwt_identity())
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    items = sorted(playlist.items, key=lambda x: x.order)
    return jsonify(
        {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "videos": [
                {
                    "id": it.video.id,
                    "title": it.video.title,
                    "description": it.video.description,
                    "url": it.video.url,
                    "duration": it.video.duration,
                    "course_title": it.video.course.title,
                    "thumbnail": it.video.thumbnail,
                    "order": it.order,
                }
                for it in items
            ],
        }
    )


@playlists_bp.route("/<int:playlist_id>/videos", methods=["POST"])
@jwt_required()
def add_video(playlist_id):
    user_id = int(get_jwt_identity())
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json() or {}
    video_id = data.get("video_id")
    if not video_id:
        return jsonify({"error": "video_id required"}), 400
    order = len(playlist.items)
    item = PlaylistItem(playlist_id=playlist_id, video_id=video_id, order=order)
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Video added", "item_count": len(playlist.items)}), 201


@playlists_bp.route("/<int:playlist_id>/videos/<int:video_id>", methods=["DELETE"])
@jwt_required()
def remove_video(playlist_id, video_id):
    user_id = int(get_jwt_identity())
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    item = PlaylistItem.query.filter_by(playlist_id=playlist_id, video_id=video_id).first()
    if not item:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Removed"})


@playlists_bp.route("/<int:playlist_id>", methods=["DELETE"])
@jwt_required()
def delete_playlist(playlist_id):
    user_id = int(get_jwt_identity())
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    PlaylistItem.query.filter_by(playlist_id=playlist_id).delete()
    db.session.delete(playlist)
    db.session.commit()
    return jsonify({"message": "Playlist deleted"})


@playlists_bp.route("/videos/all", methods=["GET"])
@jwt_required()
def all_videos():
    videos = Video.query.all()
    return jsonify(
        {
            "videos": [
                {
                    "id": v.id,
                    "title": v.title,
                    "course_title": v.course.title,
                    "duration": v.duration,
                    "url": v.url,
                    "thumbnail": v.thumbnail,
                }
                for v in videos
            ]
        }
    )
