import os
from flask import Flask, jsonify
from config import Config
from extensions import db, jwt, bcrypt, cors
from routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


    # Register blueprints
    register_blueprints(app)

    @app.route("/")
    def index():
        return jsonify({"message": "MOOC Platform API is running", "version": "1.0"})

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    # Create tables + seed
    with app.app_context():
        db.create_all()
        from routes.seed_data import seed

        seed()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
