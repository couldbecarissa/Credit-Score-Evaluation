import numpy as np

# Constants
MIN_LOAN_AMOUNT = 50000
MAX_LOAN_AMOUNT = 500000
MIN_CREDIT_SCORE = 0.3

def normalize_business_duration(months_in_business):
    if months_in_business < 12:  # Less than 1 year
        return 0.2
    elif months_in_business < 36:  # 1-3 years
        return 0.4
    elif months_in_business < 60:  # 3-5 years
        return 0.6
    elif months_in_business < 120:  # 5-10 years
        return 0.8
    else:  # More than 10 years
        return 1.0

def normalize_payment_methods(methods):
    score = 0
    if 'cash' in methods:
        score += 0.3
    if 'mobile_money' in methods:
        score += 0.5
    if 'bank' in methods:
        score += 0.7
    return min(score, 1.0)

def normalize_age(age):
    if age < 25:
        return 0.3
    elif age < 35:
        return 0.6
    elif age < 50:
        return 1.0
    else:
        return 0.8

def normalize_revenue(monthly_revenue):
    if monthly_revenue < 100000:  # Less than 100,000 TSh
        return 0.2
    elif monthly_revenue < 300000:  # 100,000 to 300,000 TSh
        return 0.4
    elif monthly_revenue < 500000:  # 300,000 to 500,000 TSh
        return 0.6
    elif monthly_revenue < 1000000:  # 500,000 to 1,000,000 TSh
        return 0.8
    else:  # Over 1,000,000 TSh
        return 1.0

def normalize_dependants(dependants):
    if dependants <= 2:
        return 1.0
    elif dependants <= 4:
        return 0.8
    elif dependants <= 6:
        return 0.6
    elif dependants <= 8:
        return 0.4
    else:
        return 0.2

def normalize_debt(debt):
    if debt < 50000:
        return 1.0
    elif debt < 100000:
        return 0.8
    elif debt < 250000:
        return 0.6
    elif debt < 400000:
        return 0.4
    elif debt < 500000:
        return 0.2
    else:
        return 0.0

def calculate_debt_to_income_ratio(monthly_income, total_debt, estimated_loan_term=12):
    if monthly_income == 0:
        return float('inf'), False
    
    estimated_monthly_debt = total_debt / estimated_loan_term
    ratio = estimated_monthly_debt / monthly_income
    is_eligible = ratio <= 1.5
    return min(ratio, 2), is_eligible

def normalize_overdue_installments(num_overdue_installments):
    if num_overdue_installments == 0:
        return 1.0
    elif num_overdue_installments == 1:
        return 0.7
    elif num_overdue_installments == 2:
        return 0.4
    elif num_overdue_installments == 3:
        return 0.2
    else:
        return 0.0

def normalize_credit_inquiries(num_credit_inquiries):
    if num_credit_inquiries == 0:
        return 1.0
    elif num_credit_inquiries == 1:
        return 0.8
    elif num_credit_inquiries == 2:
        return 0.6
    elif num_credit_inquiries == 3:
        return 0.4
    else:
        return 0.2

def normalize_rgp(region_gdp, national_average_gdp):
    ratio = region_gdp / national_average_gdp
    return min(max(ratio, 0), 1)

def calculate_credit_score(user):
    weights = {
        'credit_utilization': 0.25,
        'payment_history': 0.35,
        'maturity_index': 0.10,
        'loan_term': 0.10,
        'credit_accounts': 0.20
    }

    credit_utilization = calculate_credit_utilization(user)
    payment_history = calculate_payment_history(user)
    maturity_index = calculate_maturity_index(user)
    loan_term = calculate_loan_term(user)
    credit_accounts = calculate_credit_accounts(user)

    credit_score = (
        weights['credit_utilization'] * credit_utilization +
        weights['payment_history'] * payment_history +
        weights['maturity_index'] * maturity_index +
        weights['loan_term'] * loan_term +
        weights['credit_accounts'] * credit_accounts
    )

    return credit_score

def calculate_credit_utilization(user):
    financial_literacy_weight = 0.10
    debt_weight = 0.60
    payment_method_weight = 0.15
    housing_weight = 0.15

    score = 0
    score += financial_literacy_weight if user.get("financial_literacy") == "yes" else 0
    score += debt_weight * normalize_debt(user.get("total_amount_in_debt", 0))
    score += payment_method_weight * normalize_payment_methods(user.get("payment_methods", []))
    score += housing_weight * (
        0.75 * normalize_dependants(user.get("num_dependants", 0)) +
        0.25 * (1 if user.get("housing_status") == "own" else 0.5 if user.get("housing_status") == "rent" else 0)
    )

    return score

def calculate_payment_history(user):
    weights = {
        'debt_to_income': 0.30,
        'overdue_installments': 0.25,
        'credit_inquiries': 0.15,
        'past_due_amount': 0.15,
        'past_due_days': 0.10,
        'regional_gdp': 0.05
    }

    monthly_income = user.get("monthly_income", 0)
    total_debt = user.get("total_amount_in_debt", 0)
    debt_to_income_ratio, is_eligible = calculate_debt_to_income_ratio(monthly_income, total_debt)

    if not is_eligible:
        return 0

    score = 0
    score += weights['debt_to_income'] * (1 - debt_to_income_ratio / 2)
    score += weights['overdue_installments'] * normalize_overdue_installments(user.get("num_overdue_installments", 0))
    score += weights['credit_inquiries'] * normalize_credit_inquiries(user.get("num_credit_inquiries", 0))
    score += weights['past_due_amount'] * (1 if user.get("max_past_due_amount", 0) == 0 or 
                                           user.get("max_past_due_amount", 0) < monthly_income else 0.4)
    score += weights['past_due_days'] * calculate_past_due_days_score(user.get("max_past_due_days", 0))
    score += weights['regional_gdp'] * normalize_rgp(user.get("region_gdp", 0), user.get("national_average_gdp", 1))

    return score

def calculate_maturity_index(user):
    business_duration_weight = 0.60
    age_weight = 0.40

    score = 0
    score += business_duration_weight * normalize_business_duration(user.get("months_in_business", 0))
    score += age_weight * normalize_age(user.get("age", 0))

    return score

def calculate_loan_term(user):
    loan_term = user.get("loan_term", 30)  # Assuming loan terms are in days
    if loan_term <= 30:
        return 1.0
    elif loan_term <= 60:
        return 0.8
    elif loan_term <= 90:
        return 0.6
    else:
        return 0.4

def calculate_credit_accounts(user):
    num_credit_accounts = user.get("num_credit_accounts", 0)
    total_open_contracts = user.get("total_open_contracts", 0)

    score = 0
    for variable in [num_credit_accounts, total_open_contracts]:
        if variable == 0:
            score += 0.5  # Neutral score for no credit history
        elif variable == 1:
            score += 1.0
        elif variable == 2:
            score += 0.8
        elif variable <= 4:
            score += 0.6
        else:
            score += 0.4

    return score / 2  # Normalize to 0-1 range

def calculate_past_due_days_score(max_past_due_days):
    if max_past_due_days == 0:
        return 1.0
    elif max_past_due_days <= 7:
        return 0.8
    elif max_past_due_days <= 14:
        return 0.6
    elif max_past_due_days <= 30:
        return 0.4
    elif max_past_due_days <= 60:
        return 0.2
    else:
        return 0.0

def approve_loan(credit_score, requested_amount):
    if credit_score <= MIN_CREDIT_SCORE:
        return 0  # No loan approved

    # Calculate maximum loan amount based on credit score
    max_approved_amount = MIN_LOAN_AMOUNT + (MAX_LOAN_AMOUNT - MIN_LOAN_AMOUNT) * credit_score

    # Approve the lesser of the requested amount and the maximum approved amount
    approved_amount = min(requested_amount, max_approved_amount)

    # Ensure the approved amount is within the allowable range
    return max(MIN_LOAN_AMOUNT, min(approved_amount, MAX_LOAN_AMOUNT))

def calculate_risk_score(user):
    weights = {
        'lack_financial_documentation': 0.15,
        'negative_credit_history': 0.25,
        'high_debt_to_income_ratio': 0.20,
        'business_instability': 0.15,
        'lack_collateral': 0.10,
        'high_risk_location': 0.05,
        'inadequate_management_experience': 0.10
    }

    risk_score = 0
    risk_score += weights['lack_financial_documentation'] * (1 if not user.get("financial_literacy") else 0)
    risk_score += weights['negative_credit_history'] * (1 - calculate_credit_accounts(user))
    risk_score += weights['high_debt_to_income_ratio'] * calculate_debt_to_income_ratio(user.get("monthly_income", 0), user.get("total_amount_in_debt", 0))[0] / 2
    risk_score += weights['business_instability'] * (1 - normalize_business_duration(user.get("months_in_business", 0)))
    risk_score += weights['lack_collateral'] * (1 if not user.get("collateral") else 0)
    risk_score += weights['high_risk_location'] * (1 - normalize_rgp(user.get("region_gdp", 0), user.get("national_average_gdp", 1)))
    risk_score += weights['inadequate_management_experience'] * (1 - calculate_maturity_index(user))

    return min(max(risk_score, 0), 1)

def is_dead_case(user):
    risk_score = calculate_risk_score(user)
    return risk_score >= 0.5

def evaluate_loan_application(user):
    if is_dead_case(user):
        return {
            "status": "Rejected",
            "reason": "High risk applicant",
            "approved_amount": 0
        }

    credit_score = calculate_credit_score(user)
    requested_amount = user.get("requested_loan_amount", 0)
    approved_amount = approve_loan(credit_score, requested_amount)

    return {
        "status": "Approved" if approved_amount > 0 else "Rejected",
        "credit_score": credit_score,
        "approved_amount": approved_amount,
        "risk_score": calculate_risk_score(user)
    }

# Example usage
if __name__ == "__main__":
    sample_user = {
        "financial_literacy": "yes",
        "total_amount_in_debt": 20,
        "payment_methods": ["cash", "mobile_money"],
        "num_dependants": 3,
        "housing_status": "rent",
        "age": 32,
        "months_in_business": 36,
        "monthly_income": 500000,
        "num_overdue_installments": 1,
        "num_credit_inquiries": 2,
        "max_past_due_amount": 50000,
        "max_past_due_days": 15,
        "num_credit_accounts": 1,
        "total_open_contracts": 1,
        "region_gdp": 2000000,
        "national_average_gdp": 2500000,
        "loan_term": 60,
        "requested_loan_amount": 300000,
        "collateral": "business inventory"
    }

    result = evaluate_loan_application(sample_user)
    print(result)