# run.py

from app import create_app, db
from app.exceptions import register_error_handlers

app = create_app()

with app.app_context():
    db.create_all()  # creates tables if they don't exist
    register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
