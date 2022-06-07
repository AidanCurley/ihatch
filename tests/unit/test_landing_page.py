"""Unit tests for the landing page of the application"""
from tests.unit import client


def test_landing_page(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert '<img src="../static/logos/iHatch-logos.jpeg" alt="logo">' in html
    assert landing.status_code == 200
