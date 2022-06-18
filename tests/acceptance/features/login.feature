Feature: Login

    As a user
      I want to be able to login to the application using my username and password.

    @fixture.browser
    Scenario: User Enters Correct Details When Logging In
        Given the user navigates to the login page
        And the user enters correct details
        When she clicks login
        Then she should be logged in and redirected to the main dashboard

    @fixture.browser
    Scenario: User Enters Incorrect Password When Logging In
        Given the user navigates to the login page
        And the user enters incorrect details
        When she clicks login
        Then an "incorrect details" error should be displayed
        And she should remain on the login page

    @fixture.browser
    Scenario: User Trying to Bypass Login Page Is Redirected to Login Page
        Given the user is not logged in
        When the user navigates to the dashboard
        Then she should be redirected to the login page

    @fixture.browser
    Scenario: User Who Is not Logged In Is Redirected to Login Page
        Given the user is not logged in
        When the user navigates to the main web address
        Then she should be redirected to the login page
