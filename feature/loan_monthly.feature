Feature: LoanMonthlyCalculator
    A tool that help user calculate their repayment amount

    Scenario: Calculate repayment amount
        Given I want to apply for a loan with conditions: 100w / 3year / 1.2%rate / 0fee 

        When I go to the loan monthly calculate page
        And I fill in all the info
        And I click the calculate button

        Then I should see the repayment amount 

