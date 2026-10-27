import os
from flask import Flask, render_template


def create_app():
    # create the app
    app = Flask(__name__)
    
    # the main page
    @app.route('/')
    def main_page():
        return render_template('index.html')

    return app