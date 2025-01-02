from config.settings import Settings
from infrastructure.database import Database
from flask import Flask
from interfaces.web.blueprints.testing.routes import setup_routes

def create_app(environment: str = 'default') -> Flask:
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Settings)
    
    # Initialize database
    db_config = Settings.get_database_config(environment)
    database = Database(db_config['url'])
    app.db = database
    
    # Register blueprints and setup routes
    setup_routes(app)
    
    return app

def init_database(app: Flask):
    """Initialize database tables"""
    with app.app_context():
        app.db.create_database()

if __name__ == "__main__":
    app = create_app()
    init_database(app)
    app.run(debug=Settings.DEBUG)