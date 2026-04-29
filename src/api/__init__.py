from flask import Flask


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="../../frontend",
        static_url_path="",
        template_folder="../../frontend",
    )

    from .routes import bp

    app.register_blueprint(bp)

    return app
