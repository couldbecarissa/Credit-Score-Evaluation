import main.normalization as normalization

def calculate_credit_score(user):
    # Define weights for main factors
    weights = {
        'credit_utilization': 0.25,
        'payment_history': 0.35,
        'maturity_index': 0.10,
        'loan_term': 0.10,
        'credit_accounts': 0.20
    }

    # Calculate individual scores
    credit_utilization = calculate_credit_utilization(user)
    payment_history = calculate_payment_history(user)
    maturity_index = calculate_maturity_index(user)
    loan_term = calculate_loan_term(user)
    credit_accounts = calculate_credit_accounts(user)

    # Calculate final credit score
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
    score += debt_weight * normalization.normalize_debt(user.get("total_amount_in_debt", 0))
    score += payment_method_weight * normalization.normalize_payment_methods(user.get("payment_methods", []))
    score += housing_weight * (
        0.75 * normalization.normalize_dependants(user.get("num_dependants", 0)) +
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
    debt_to_income_ratio, is_eligible = normalization.calculate_debt_to_income_ratio(monthly_income, total_debt)

    if not is_eligible:
        return 0  # Return 0 if debt-to-income ratio is above 1.5


    score = 0
    score += weights['debt_to_income'] * (1 - debt_to_income_ratio / 2)  # Normalize the ratio
    score += weights['overdue_installments'] * normalization.normalize_overdue_installments(user.get("num_overdue_installments", 0))
    score += weights['credit_inquiries'] * normalization.normalize_credit_inquiries(user.get("num_credit_inquiries", 0))
    score += weights['past_due_amount'] * (1 if user.get("max_past_due_amount", 0) == 0 or 
                                           user.get("max_past_due_amount", 0) < monthly_income else 0.4)
    score += weights['past_due_days'] * calculate_past_due_days_score(user.get("max_past_due_days", 0))
    score += weights['regional_gdp'] * normalization.normalize_rgp(user.get("region_gdp", 0), user.get("national_average_gdp", 1))

    return score

def calculate_maturity_index(user):
    business_duration_weight = 0.60
    age_weight = 0.40

    score = 0
    score += business_duration_weight * normalization.normalize_business_duration(user.get("months_in_business", 0))
    score += age_weight * normalization.normalize_age(user.get("age", 0))

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
    min_loan_amount = 50000
    max_loan_amount = 500000
    min_credit_score = 0.3

    if credit_score <= min_credit_score:
        return 0  # No loan approved

    # Calculate maximum loan amount based on credit score
    max_approved_amount = min_loan_amount + (max_loan_amount - min_loan_amount) * credit_score

    # Approve the lesser of the requested amount and the maximum approved amount
    approved_amount = min(requested_amount, max_approved_amount)

    # Ensure the approved amount is within the allowable range
    return max(min_loan_amount, min(approved_amount, max_loan_amount))

def should_calculate(user):
    monthly_income = user.get("monthly_income", 0)
    monthly_debt = user.get("monthly_debt", 0)
    _, is_eligible = normalization.calculate_debt_to_income_ratio(monthly_income, monthly_debt)

    if not is_eligible:
        raise ValueError("You are not eligible for a loan due to a high debt-to-income ratio")

    return calculate_credit_score(user)