"""Set up the test environment for Flask by hosting our flask web app on a chrome server
Inspired by: https://medium.com/@sannidhi.s.t/bdd-for-flask-application-using-behave-selenium-fc6ec338c0e6
"""

import threading
from behave import fixture, use_fixture
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from flaskr.main import app

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")


@fixture
def browser(context, **kwargs):
    """Creates and returns a browser using Chrome web driver"""
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    context.browser = browser
    return browser


def before_tag(context, tag):
    """Enables the use of fixtures using tags"""
    if tag == "fixture.browser":
        use_fixture(browser, context)


def before_all(context):
    """Sets up a server and our app"""
    context.server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()


def after_all(context):
    """Clears everything after all tests have been run"""
    context.server.shutdown()
    context.pa_app.join()