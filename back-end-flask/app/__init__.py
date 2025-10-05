from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importa e registra nosso Blueprint de rotas da API
    from .api.main_routes import api_bp

    app.register_blueprint(api_bp)

    return app