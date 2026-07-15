from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Message, User
from datetime import datetime

messages_bp = Blueprint("messages", __name__)


def _serialize(m):
    return {
        "id": m.id,
        "sender_id": m.sender_id,
        "sender_name": m.sender.full_name or m.sender.username,
        "receiver_id": m.receiver_id,
        "receiver_name": m.receiver.full_name or m.receiver.username,
        "content": m.content,
        "is_read": m.is_read,
        "created_at": m.created_at.isoformat(),
    }


@messages_bp.route("/conversations", methods=["GET"])
@jwt_required()
def conversations():
    user_id = int(get_jwt_identity())
    # distinct users
    sent = Message.query.filter_by(sender_id=user_id).all()
    received = Message.query.filter_by(receiver_id=user_id).all()
    user_ids = set()
    for m in sent + received:
        other = m.receiver_id if m.sender_id == user_id else m.sender_id
        user_ids.add(other)

    conversations = []
    for other_id in user_ids:
        other = User.query.get(other_id)
        last_msg = (
            Message.query.filter(
                ((Message.sender_id == user_id) & (Message.receiver_id == other_id))
                | ((Message.sender_id == other_id) & (Message.receiver_id == user_id))
            )
            .order_by(Message.created_at.desc())
            .first()
        )
        unread = Message.query.filter_by(
            sender_id=other_id, receiver_id=user_id, is_read=False
        ).count()
        conversations.append(
            {
                "other_user": {
                    "id": other.id,
                    "username": other.username,
                    "full_name": other.full_name,
                    "avatar": other.avatar,
                },
                "last_message": _serialize(last_msg) if last_msg else None,
                "unread": unread,
            }
        )
    conversations.sort(key=lambda x: x["last_message"]["created_at"] if x["last_message"] else "", reverse=True)
    return jsonify({"conversations": conversations})


@messages_bp.route("/with/<int:other_id>", methods=["GET"])
@jwt_required()
def conversation_with(other_id):
    user_id = int(get_jwt_identity())
    msgs = (
        Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == other_id))
            | ((Message.sender_id == other_id) & (Message.receiver_id == user_id))
        )
        .order_by(Message.created_at.asc())
        .all()
    )
    # mark received as read
    for m in msgs:
        if m.receiver_id == user_id and not m.is_read:
            m.is_read = True
    db.session.commit()
    return jsonify({"messages": [_serialize(m) for m in msgs]})


@messages_bp.route("", methods=["POST"])
@jwt_required()
def send_message():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    receiver_id = data.get("receiver_id")
    content = (data.get("content") or "").strip()
    if not receiver_id or not content:
        return jsonify({"error": "receiver_id and content required"}), 400
    msg = Message(sender_id=user_id, receiver_id=receiver_id, content=content)
    db.session.add(msg)
    db.session.commit()
    return jsonify(_serialize(msg)), 201


@messages_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    user_id = int(get_jwt_identity())
    users = User.query.filter(User.id != user_id).all()
    return jsonify(
        {
            "users": [
                {
                    "id": u.id,
                    "username": u.username,
                    "full_name": u.full_name,
                    "avatar": u.avatar,
                }
                for u in users
            ]
        }
    )
