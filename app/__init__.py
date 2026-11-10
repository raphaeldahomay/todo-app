import os
from flask import Flask


def create_app():
    # create the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    
    from app.routes import main
    app.register_blueprint(main)

    return app