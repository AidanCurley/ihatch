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
@then('she should be redirected to the login page')
def step_impl(context):
    context.browser.get('http://www.ihatch.uk/login')


@given('the user navigates to the register page')
def step_impl(context):
    context.browser.get('http://www.ihatch.uk/register')


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


@given('an account exists for a username')
def step_impl(context):
    pass


@given('she clicks login')
@when('she clicks login')
def step_impl(context):
    login_button = context.browser.find_element_by_id('login')
    login_button.click()


@when('she clicks register in the menu')
def step_impl(context):
    context.browser.find_element_by_link_text('Register').click()


@when('she clicks I have forgotten my password')
def step_impl(context):
    password_button = context.browser.find_element_by_id('forgot_password')
    password_button.click()


@when('she enters her details and clicks the \'Register\' button')
def step_impl(context):
    username = context.browser.find_element_by_id('username')
    password = context.browser.find_element_by_id('pass')
    confirm_password = context.browser.find_element_by_id('confirm-pass')
    f_name = context.browser.find_element_by_id('f_name')
    surname = context.browser.find_element_by_id('surname')
    email = context.browser.find_element_by_id('email')
    ts_and_cs = context.browser.find_element_by_id('privacy')
    register_button = context.browser.find_element_by_id('submit')

    username.send_keys('Test User')
    password.send_keys('123456')
    confirm_password.send_keys('123456')
    f_name.send_keys('name')
    surname.send_keys('surname')
    email.send_keys('email@email.com')
    ts_and_cs.click()
    register_button.click()


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


@then('she should remain on the register page')
def step_impl(context):
    assert context.browser.current_url == 'http://www.ihatch.uk/register'


@then('a \'username exists\' error should be displayed')
def step_impl(context):
    assert 'There is already an account associated with this username.' in context.browser.page_source


@then('she will be sent a password reminder')
def step_impl(context):
    pass
