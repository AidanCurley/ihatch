
Feature: Create a New Account

  As a user
    I want to be able to request a password reminder if I have forgotten my password.
    It should be sent by email.

  Scenario: User Requests Forgotten Password
      Given the user navigates to the login page
       When she clicks I have forgotten my password
       Then she will be sent a password reminder
