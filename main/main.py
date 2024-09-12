from flask import Flask, render_template
import credit_risk_evaluation
import normalization

app = Flask(__name__)

@app.route('/')
def loan_evaluation():
    user1 = {
        "financial_literacy": "yes",
        "total_amount_in_debt": 2000000,
        "payment_methods": ["cash"],
        "num_dependants": 3,
        "housing_status": "rent",
        "age": 32,
        "months_in_business": 96,
        "monthly_income": 700000,
        "num_overdue_installments": 1,
        "num_credit_inquiries": 2,
        "max_past_due_amount": 60000,
        "max_past_due_days": 30,
        "num_credit_accounts": 6,
        "total_open_contracts": 12,
        "region_gdp": 2000000,
        "national_average_gdp": 2000000,
        "loan_term": 30,
        "requested_loan_amount": 300000
    }

    # Calculate credit score
    credit_score = credit_risk_evaluation.should_calculate(user=user1)
    
    # Calculate debt-to-income ratio and eligibility
    debt_to_income_ratio, is_eligible = normalization.calculate_debt_to_income_ratio(
        user1["monthly_income"], user1["total_amount_in_debt"]
    )
    
    # If eligible, calculate the approved loan amount, otherwise set to 0
    approved_loan = credit_risk_evaluation.approve_loan(credit_score, user1["requested_loan_amount"]) if is_eligible else 0

    # Pass results to the template
    return render_template(
        'loan_evaluation.html', 
        user=user1, 
        credit_score=round(credit_score, 3), 
        debt_to_income_ratio=round(debt_to_income_ratio, 2), 
        is_eligible=is_eligible, 
        approved_loan=approved_loan
    )

if __name__ == '__main__':
    app.run(debug=True)
