import os
from flask import Flask


def create_app():
    # create the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    
    from app.auth_routes import main
    from app import action_routes
    app.register_blueprint(main)

    return app