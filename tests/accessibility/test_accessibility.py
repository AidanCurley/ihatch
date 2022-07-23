"""Accessibility Tests for each of the application pages"""
from axe_selenium_python import Axe
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-proxy-server')


def test_landing_page_accessibility():
    """Tests the accessibility of the landing page"""
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://51.142.124.189:5000/")

    axe = Axe(driver)
    axe.inject()
    results = axe.run()

    axe.write_results(results, 'results.json')

    # Should be no violations
    assert len(results["violations"]) == 0, axe.report(results["violations"])

    driver.quit()
