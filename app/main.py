"""Launch the application"""
from datetime import datetime

from flask import request, jsonify, make_response, Response, render_template

from app import create_app, db
from app.models import User, Sensor, Hatch, Egg, Weight, Measurement

app = create_app('development')


@app.route('/')
def landing_page():
    """Controller for the landing page route"""
    return render_template('landing.html')


if __name__ == "__main__":
    app.run()
