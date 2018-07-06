from flask import Flask
from flask_cors import CORS

# Flask extensions
cors = CORS()


def create_app(config):
    app = Flask(__name__)

    # Config app
    app.config.from_object(config)

    # Flask-Cors
    cors.init_app(app)

    # Register blueprints
    from ebi_image_service.handlers.image import image_bp

    # Register blueprints
    app.register_blueprint(image_bp)

    print(app.url_map)

    return app
