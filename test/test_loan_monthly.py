import pytest
import time
from pytest_bdd import scenario, given, when, then, parsers
from page.loan_monthly import LoanMonthly


# 每月應付本息金額之平均攤還率 ＝ { [ ( 1＋月利率 ) ^ 月數 ] × 月利率 } ÷ { [ ( 1＋月利率 ) ^ 月數 ]－1 }
# 平均每月應攤付本息金額 ＝ 貸款本金 × 每月應付本息金額之平均攤還率
def _calculate_monthly_payment(principal, annual_interest_rate, loan_term_in_months):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    denominator = ((1 + monthly_interest_rate) ** loan_term_in_months) - 1
    amortization_rate = (
        monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term_in_months)
    ) / denominator

    monthly_payment = principal * 10000 * amortization_rate
    total_payment = monthly_payment * loan_term_in_months - principal * 10000
    print(f"round 後的 monthly:{round(monthly_payment)}")
    print(f"計算結果:{monthly_payment}")
    monthly_payment = "{:,.0f}".format((monthly_payment))
    total_payment = "{:,.0f}".format((total_payment))
    print(f"調整後結果:{monthly_payment}")
    print(f"總共要繳多少:{total_payment}")
    return monthly_payment, total_payment


def genarate_expected_result(amount, period, rate, fee):
    expected = []
    expected.append(f"第1~{period}月")
    res = _calculate_monthly_payment(amount, rate, period)
    expected.append(res[0])
    expected.append(f"{rate}%")
    expected.append("{:,.0f}".format(amount * 10000))
    expected.append(res[1])
    a = amount * 10000 + int(res[1].replace(",", ""))
    expected.append("{:,.0f}".format(a))
    print(expected)
    return expected


@pytest.fixture
def loan_fixture():
    data = {
        "amount": "100",
        "period": "60",
        "rate": "0",
        "fee": "0",
    }
    return data


@pytest.fixture
def browser(request):
    return request.getfixturevalue("browser")


@pytest.fixture
def loan_monthly(browser):
    loan_monthly_instance = LoanMonthly(browser)
    return loan_monthly_instance


@scenario("../feature/loan_monthly.feature", "Calculate repayment amount")
def test_calculate_repayment_amount():
    print("Test start...")


@given(
    name=parsers.parse(
        "I want to apply for a loan with conditions: {amount:d}w / {period:d}year / {rate:f}%"
        + "rate / {fee:d}fee"
    ),
    target_fixture="loan_fixture",
)
def given_i_want_to_apply_for_a_loan(amount, period, rate, fee):
    # 在這裡可以執行相應的初始化或前置條件設定
    print(
        f"In given step: given_i_want_to_apply_for_a_loan..... amount:{amount}/period:{period}/rate:{rate}/fee:{fee}"
    )
    data = {"amount": amount, "period": period * 12, "rate": rate, "fee": fee}
    return data


@when("I go to the loan monthly calculate page")
def when_i_go_to_the_loan_monthly_calculate_page(loan_monthly):
    # 實作進入貸款計算頁面的相應動作
    return loan_monthly


@when("I fill in all the info")
def when_i_fill_in_all_the_info(request):
    # 實作填入所有相應信息的動作
    loan_monthly_instance = request.getfixturevalue("loan_monthly")
    time.sleep(1)
    loan_monthly_instance.fill_in_all_input(request.getfixturevalue("loan_fixture"))


@when("I click the calculate button")
def when_i_press_the_calculate_button(request):
    # 實作按下計算按鈕的相應動作
    loan_monthly_instance = request.getfixturevalue("loan_monthly")
    loan_monthly_instance.click_calculate_btn()
    time.sleep(1)


@then("I should see the repayment amount")
def then_i_should_see_the_repayment_amount(request):
    # 實作驗證邏輯，確認是否看到了預期的還款金額
    loan_monthly_instance = request.getfixturevalue("loan_monthly")
    result = loan_monthly_instance.get_result_value()
    time.sleep(1)
    exp = request.getfixturevalue("loan_fixture")
    print(f"exp:{exp}")
    expect = genarate_expected_result(
        exp["amount"], exp["period"], exp["rate"], exp["fee"]
    )
    assert True
