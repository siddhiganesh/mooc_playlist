import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from extensions import db
from models import Video, Subtitle

ai_bp = Blueprint("ai", __name__)

# Configure Gemini
if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None


def generate_ai_response(prompt):
    """Generic Gemini caller with graceful fallback."""
    if not model:
        return (
            "AI service is not configured. Please set your GEMINI_API_KEY in backend/.env. "
            "Here is a placeholder summary based on the input you provided."
        )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI service error: {str(e)}"


@ai_bp.route("/summarize", methods=["POST"])
@jwt_required()
def summarize():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    video_id = data.get("video_id")

    if video_id and not text:
        subtitles = Subtitle.query.filter_by(video_id=video_id).all()
        if subtitles:
            text = " ".join(s.content for s in subtitles)
        else:
            video = Video.query.get(video_id)
            if video:
                text = video.description or video.title

    if not text:
        return jsonify({"error": "No text to summarize"}), 400

    prompt = (
        "Please provide a clear, structured summary of the following educational content. "
        "Use bullet points and key takeaways. Keep it concise (around 200-300 words):\n\n"
        f"{text}"
    )
    summary = generate_ai_response(prompt)
    return jsonify({"summary": summary, "source_length": len(text)})


@ai_bp.route("/keypoints", methods=["POST"])
@jwt_required()
def keypoints():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    video_id = data.get("video_id")

    if video_id and not text:
        subtitles = Subtitle.query.filter_by(video_id=video_id).all()
        if subtitles:
            text = " ".join(s.content for s in subtitles)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = (
        "Extract the top 7-10 key learning points from this educational content. "
        "Format as a numbered list with short, clear statements:\n\n"
        f"{text}"
    )
    points = generate_ai_response(prompt)
    return jsonify({"keypoints": points})


@ai_bp.route("/explain", methods=["POST"])
@jwt_required()
def explain():
    data = request.get_json() or {}
    topic = data.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Topic required"}), 400

    prompt = (
        f"Explain the following concept in simple terms for a student. "
        f"Include a short definition, an analogy, and 2-3 examples:\n\nTopic: {topic}"
    )
    explanation = generate_ai_response(prompt)
    return jsonify({"explanation": explanation})


@ai_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    context = data.get("context", "")
    if not message:
        return jsonify({"error": "Message required"}), 400

    prompt = (
        f"You are a helpful teaching assistant for an online learning platform. "
        f"Context: {context}\n\nStudent: {message}\n\nAssistant:"
    )
    reply = generate_ai_response(prompt)
    return jsonify({"reply": reply})


@ai_bp.route("/generate-quiz", methods=["POST"])
@jwt_required()
def generate_quiz():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    video_id = data.get("video_id")
    num_questions = int(data.get("num_questions", 5))

    if video_id and not text:
        subtitles = Subtitle.query.filter_by(video_id=video_id).all()
        if subtitles:
            text = " ".join(s.content for s in subtitles)

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = (
        f"Generate {num_questions} multiple-choice questions (4 options each) "
        f"from the following content. Return ONLY valid JSON in this exact format:\n"
        f'{{"questions":[{{"question":"...","options":["A","B","C","D"],"answer":0}}]}}\n\n'
        f"Content:\n{text}"
    )
    raw = generate_ai_response(prompt)
    return jsonify({"raw": raw})
