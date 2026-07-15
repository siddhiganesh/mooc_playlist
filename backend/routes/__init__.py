from .auth import auth_bp
from .courses import courses_bp
from .playlists import playlists_bp
from .ai import ai_bp
from .subtitles import subtitles_bp
from .assignments import assignments_bp
from .quizzes import quizzes_bp
from .notes import notes_bp
from .discussion import discussion_bp
from .certificates import certificates_bp
from .leaderboard import leaderboard_bp
from .messages import messages_bp
from .profile import profile_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(courses_bp, url_prefix="/api/courses")
    app.register_blueprint(playlists_bp, url_prefix="/api/playlists")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(subtitles_bp, url_prefix="/api/subtitles")
    app.register_blueprint(assignments_bp, url_prefix="/api/assignments")
    app.register_blueprint(quizzes_bp, url_prefix="/api/quizzes")
    app.register_blueprint(notes_bp, url_prefix="/api/notes")
    app.register_blueprint(discussion_bp, url_prefix="/api/discussion")
    app.register_blueprint(certificates_bp, url_prefix="/api/certificates")
    app.register_blueprint(leaderboard_bp, url_prefix="/api/leaderboard")
    app.register_blueprint(messages_bp, url_prefix="/api/messages")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
