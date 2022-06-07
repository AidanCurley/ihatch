"""Launch the application"""
from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)


@app.route('/')
def landing_page():
    """Controller for the landing page route"""
    return render_template('landing.html')


if __name__ == '__main__':
    app.run()
