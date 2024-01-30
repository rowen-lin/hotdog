import pytest
import time
from pytest_bdd import scenario, given, when, then
from page.loan_monthly import LoanMonthly


@pytest.fixture
def loan_fixture():
    loan = {
        "amount": "100",
        "period": "60",
        "rate": "0",
        "fee": "0",
        "expected": ["第1~60月", "16,667", "0%", "1,000,000", "0", "1,000,000"],
    }
    return loan


@pytest.fixture
def browser(request):
    return request.getfixturevalue("browser")


@pytest.fixture
def loan_monthly(browser):
    loan_monthly_instance = LoanMonthly(browser)
    return loan_monthly_instance


@scenario("./loan_monthly.feature", "Calculate repayment amount")
def test_calculate_repayment_amount():
    pass


@given("I want to apply for a loan with conditions: 50w / 3year / 1.2% rate / 3000 fee")
def given_i_want_to_apply_for_a_loan(loan_fixture):
    # 在這裡可以執行相應的初始化或前置條件設定
    return loan_fixture
    pass


@when("I go to the loan monthly calculate page")
def when_i_go_to_the_loan_monthly_calculate_page(loan_monthly):
    # 實作進入貸款計算頁面的相應動作
    return loan_monthly


@when("I fill in all the info")
def when_i_fill_in_all_the_info(request, loan_fixture):
    # 實作填入所有相應信息的動作
    loan_monthly_instance = request.getfixturevalue("loan_monthly")
    time.sleep(1)
    loan_monthly_instance.fill_in_all_input(loan_fixture)
    pass


@when("I click the calculate button")
def when_i_press_the_calculate_button(request):
    # 實作按下計算按鈕的相應動作
    loan_monthly_instance = request.getfixturevalue("loan_monthly")
    loan_monthly_instance.click_calculate_btn()
    time.sleep(1)
    pass


# 使用 @then 裝飾器來定義 Then 步驟
@then("I should see the repayment amount")
def then_i_should_see_the_repayment_amount(request, loan_fixture):
    # 實作驗證邏輯，確認是否看到了預期的還款金額
    loan_monthly_instance = request.getfixturevalue("loan_monthly")
    result = loan_monthly_instance.get_result_value()
    time.sleep(1)
    assert result == loan_fixture["expected"]
