from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DB_HOST = 'localhost',
        DB_USER = 'lh',
        DB_PASSWORD = '12345',
        DB_NAME = 'web_movie'
    )

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    

    return app

    

