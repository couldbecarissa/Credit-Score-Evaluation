import numpy as np
from main.credit_risk_evaluation import should_calculate, approve_loan
import main.normalization as normalization

# Sample user data
user1 = {
    "financial_literacy": "yes",
    "total_amount_in_debt": 200000,
    "payment_methods": ["cash"],
    "num_dependants": 3,
    "housing_status": "rent",
    "age": 32,
    "months_in_business": 96,  # 8 years * 12 months
    "monthly_income": 700000,  # Adjusted to a more realistic amount for the debt ratio
    "num_overdue_installments": 1,  # Adjusted from 30 to a more realistic number
    "num_credit_inquiries": 2,
    "max_past_due_amount": 60000,
    "max_past_due_days": 1,
    "num_credit_accounts": 6,
    "total_open_contracts": 1,
    "region_gdp": 2000000,  # Example GDP for Morogoro
    "national_average_gdp": 2500000,  # Example national average GDP
    "loan_term": 30,  # Adjusted to 30 days
    "requested_loan_amount": 300000  # Example requested loan amount
}

# Calculate credit score
try:
    credit_score = should_calculate(user=user1)
    print(f"User Credit Score: {np.round(credit_score, decimals=3):.3f}")

    # Calculate debt-to-income ratio
    debt_to_income_ratio, is_eligible = normalization.calculate_debt_to_income_ratio(
        user1["monthly_income"], user1["total_amount_in_debt"]
    )
    print(f"Debt-to-Income Ratio: {debt_to_income_ratio:.2f}")
    print(f"Is Eligible Based on Debt-to-Income Ratio: {is_eligible}")

    # Approve loan
    if is_eligible:
        loan_amount = approve_loan(credit_score, user1["requested_loan_amount"])
        print(f"Approved Loan Amount: {loan_amount:,.0f} TSh")
    else:
        print("Loan not approved due to high debt-to-income ratio")

except ValueError as e:
    print(f"Error: {str(e)}")

# Additional test cases
test_cases = [
    {
        "description": "High debt-to-income ratio",
        "monthly_income": 300000,
        "monthly_debt": 500000,
        "requested_loan_amount": 200000
    },
    {
        "description": "Low credit score",
        "financial_literacy": "no",
        "total_amount_in_debt": 400000,
        "payment_methods": ["cash"],
        "num_dependants": 5,
        "housing_status": "rent",
        "age": 22,
        "months_in_business": 3,
        "monthly_income": 200000,
        "monthly_debt": 100000,
        "num_overdue_installments": 3,
        "num_credit_inquiries": 5,
        "max_past_due_amount": 100000,
        "max_past_due_days": 60,
        "num_credit_accounts": 1,
        "total_open_contracts": 2,
        "region_gdp": 1500000,
        "national_average_gdp": 2500000,
        "loan_term": 90,
        "requested_loan_amount": 400000
    },
    {
        "description": "Excellent credit profile",
        "financial_literacy": "yes",
        "total_amount_in_debt": 50000,
        "payment_methods": ["bank", "mobile_money"],
        "num_dependants": 2,
        "housing_status": "own",
        "age": 40,
        "months_in_business": 60,
        "monthly_income": 1000000,
        "monthly_debt": 100000,
        "num_overdue_installments": 0,
        "num_credit_inquiries": 1,
        "max_past_due_amount": 0,
        "max_past_due_days": 0,
        "num_credit_accounts": 2,
        "total_open_contracts": 1,
        "region_gdp": 3000000,
        "national_average_gdp": 2500000,
        "loan_term": 30,
        "requested_loan_amount": 500000
    }
]

for case in test_cases:
    print(f"\nTest Case: {case['description']}")
    try:
        credit_score = should_calculate(user=case)
        print(f"Credit Score: {np.round(credit_score, decimals=3):.3f}")

        debt_to_income_ratio, is_eligible = normalization.calculate_debt_to_income_ratio(
            case["monthly_income"], case["monthly_debt"]
        )
        print(f"Debt-to-Income Ratio: {debt_to_income_ratio:.2f}")
        print(f"Is Eligible Based on Debt-to-Income Ratio: {is_eligible}")

        if is_eligible:
            loan_amount = approve_loan(credit_score, case["requested_loan_amount"])
            print(f"Approved Loan Amount: {loan_amount:,.0f} TSh")
        else:
            print("Loan not approved due to high debt-to-income ratio")

    except ValueError as e:
        print(f"Error: {str(e)}")