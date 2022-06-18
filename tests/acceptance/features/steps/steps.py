"""The implementation for each of the steps used in the features test files"""

from behave import given, when, then

# pylint: disable=missing-function-docstring
# pylint: disable=function-redefined
from flaskr.constants.messages import INCORRECT_DETAILS


@given('the user is on the main landing page')
def step_impl(context):
    context.browser.get('http://www.ihatch.uk/')


@given('the user is not logged in')
def step_impl(context):
    """this function is empty because we don't want the app to do anything here"""
    pass


@given('the user navigates to the login page')
def step_impl(context):
    context.browser.get('http://www.ihatch.uk/login')


@given('the user enters correct details')
def step_impl(context):
    username = context.browser.find_element_by_id('username')
    password = context.browser.find_element_by_id('password')
    username.send_keys('kbarron')
    password.send_keys('ssdgroup3')


@given('the user enters incorrect details')
def step_impl(context):
    username = context.browser.find_element_by_id('username')
    password = context.browser.find_element_by_id('password')
    username.send_keys('!@#$')
    password.send_keys('secret')


@given('she clicks login')
@when('she clicks login')
def step_impl(context):
    login_button = context.browser.find_element_by_id('login')
    login_button.click()


@when('the user navigates to the dashboard')
def step_impl(context):
    context.browser.get('http://www.ihatch.uk/dashboard')


@when('the user navigates to the main web address')
def step_impl(context):
    context.browser.get('http://www.ihatch.uk/')


@when('she clicks logout')
def step_impl(context):
    logout_button = context.browser.find_element_by_id('logout')
    logout_button.click()


@then('she should be logged in and redirected to the main dashboard')
def step_impl(context):
    assert context.browser.current_url == 'http://www.ihatch.uk//dashboard'
    assert 'Welcome' in context.browser.page_source


@then('she should remain on the login page')
def step_impl(context):
    assert context.browser.current_url == 'http://www.ihatch.uk/login'


@then('an "incorrect details" error should be displayed')
def step_impl(context):
    assert INCORRECT_DETAILS in context.browser.page_source


@then('she should be redirected to the login page')
def step_impl(context):
    assert context.browser.current_url == 'http://www.ihatch.uk/login'
