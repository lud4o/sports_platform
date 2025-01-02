from src.interfaces.web import create_app, db

app = create_app()

# Create tables on startup if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)