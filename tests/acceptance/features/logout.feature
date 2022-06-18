Feature: Logout

    As a user
      I want to be able to logout of the application.

    @fixture.browser
    Scenario: User Clocks Logout
        Given the user navigates to the login page
        And the user enters correct details
        And she clicks login
        When she clicks logout
        Then she should be redirected to the login page
