import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Quiz, QuizAttempt, Test, Course, Enrollment
from datetime import datetime

quizzes_bp = Blueprint("quizzes", __name__)


def _parse_questions(raw):
    try:
        return json.loads(raw) if raw else []
    except Exception:
        return []


@quizzes_bp.route("", methods=["GET"])
@jwt_required()
def list_quizzes():
    user_id = int(get_jwt_identity())
    enrolled_ids = [e.course_id for e in Enrollment.query.filter_by(user_id=user_id).all()]
    if not enrolled_ids:
        return jsonify({"quizzes": []})
    quizzes = Quiz.query.filter(Quiz.course_id.in_(enrolled_ids)).all()
    return jsonify(
        {
            "quizzes": [
                {
                    "id": q.id,
                    "title": q.title,
                    "description": q.description,
                    "course_title": q.course.title,
                    "time_limit": q.time_limit,
                    "question_count": len(_parse_questions(q.questions)),
                }
                for q in quizzes
            ]
        }
    )


@quizzes_bp.route("/<int:quiz_id>", methods=["GET"])
@jwt_required()
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = _parse_questions(quiz.questions)
    # strip answer key for students
    safe_questions = [
        {"question": q.get("question", ""), "options": q.get("options", [])} for q in questions
    ]
    return jsonify(
        {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "course_title": quiz.course.title,
            "time_limit": quiz.time_limit,
            "questions": safe_questions,
        }
    )


@quizzes_bp.route("/<int:quiz_id>/submit", methods=["POST"])
@jwt_required()
def submit_quiz(quiz_id):
    user_id = int(get_jwt_identity())
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json() or {}
    answers = data.get("answers", [])
    questions = _parse_questions(quiz.questions)

    if not questions:
        return jsonify({"error": "Quiz has no questions"}), 400

    correct = 0
    for i, q in enumerate(questions):
        if i < len(answers) and int(answers[i]) == int(q.get("answer", -1)):
            correct += 1
    score = (correct / len(questions)) * 100.0

    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=user_id,
        score=score,
        answers=json.dumps(answers),
    )
    db.session.add(attempt)
    # reward points
    from models import User
    user = User.query.get(user_id)
    user.points = (user.points or 0) + int(score)
    db.session.commit()

    return jsonify(
        {
            "score": score,
            "correct": correct,
            "total": len(questions),
            "attempted_at": attempt.attempted_at.isoformat(),
        }
    )


@quizzes_bp.route("/tests", methods=["GET"])
@jwt_required()
def list_tests():
    user_id = int(get_jwt_identity())
    enrolled_ids = [e.course_id for e in Enrollment.query.filter_by(user_id=user_id).all()]
    if not enrolled_ids:
        return jsonify({"tests": []})
    tests = Test.query.filter(Test.course_id.in_(enrolled_ids)).all()
    return jsonify(
        {
            "tests": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "course_title": t.course.title,
                    "total_marks": t.total_marks,
                }
                for t in tests
            ]
        }
    )


@quizzes_bp.route("/tests/<int:test_id>", methods=["GET"])
@jwt_required()
def get_test(test_id):
    test = Test.query.get_or_404(test_id)
    questions = _parse_questions(test.questions)
    return jsonify(
        {
            "id": test.id,
            "title": test.title,
            "description": test.description,
            "course_title": test.course.title,
            "total_marks": test.total_marks,
            "questions": questions,
        }
    )
