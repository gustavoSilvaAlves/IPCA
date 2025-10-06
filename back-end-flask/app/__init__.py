from flask import Flask
import logging


def create_app():
    app = Flask(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]'
    )

    from .api.main_routes import api_bp

    app.register_blueprint(api_bp)
    app.logger.info("Aplicação backend iniciada.")
    return app