from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import app as routes_app

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(routes_app)


# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    # Use your existing function to find a user by ID
    return User.query.get(user_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
