from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config.settings import Settings

db = SQLAlchemy()

def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = Settings.get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from .api.athletes import athlete_bp
    from .api.tests import test_bp
    from .api.analysis import analysis_bp
    
    app.register_blueprint(athlete_bp, url_prefix='/api/athletes')
    app.register_blueprint(test_bp, url_prefix='/api/tests')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    
    return app