from . import (
    normalize_age,
    normalize_business_duration,
    normalize_credit_inquiries,
    normalize_debt,
    normalize_debt_to_income_ratio,
    normalize_dependants,
    normalize_housing_status,
    normalize_open_contracts,
    normalize_overdue_installments,
    normalize_payment_methods,
    normalize_revenue,
    normalize_rgp,
    calculate_debt_to_income_ratio,
    calculate_past_due_days_score,
)


def calculate_credit_score(user):
    # Weights assigned to the feature categories
    weights = {"high_features": 0.70, "middle_features": 0.20, "low_features": 0.10}

    # Calculate high, middle, and low feature scores
    high_features = calculate_high_features(user)
    middle_features = calculate_middle_features(user)
    low_features = calculate_low_features(user)

    # If high features score is 0 due to a disqualifying factor like DTI ratio, return 0
    if high_features == 0:
        return 0

    # Calculate the final credit score based on weighted features
    credit_score = (
        weights["high_features"] * high_features
        + weights["middle_features"] * middle_features
        + weights["low_features"] * low_features
    )

    return credit_score


def calculate_high_features(user):
    # Weights assigned to high impact features
    weights = {
        "debt": 0.30,
        "average_monthly_revenue": 0.30,
        "past_due_amount": 0.10,
        "overdue_installments": 0.10,
        "open_contract": 0.05,
        "past_due_days": 0.05,
        "debt_to_income_ratio": 0.10,
    }

    # Extract user financial data
    monthly_revenue = user.get("average_monthly_revenue", 0)
    total_debt = user.get("total_amount_in_debt", 0)
    monthly_income = user.get("monthly_income", 0)

    # Calculate the debt-to-revenue ratio
    debt_to_revenue_ratio = calculate_debt_to_revenue_ratio(total_debt, monthly_revenue)

    # Disqualify user if the debt-to-revenue ratio is 0.8 or higher
    if debt_to_revenue_ratio >= 0.8:
        return 0  # Disqualify user by setting high_features to 0

    # Proceed with regular scoring if user passes the eligibility check
    score = 0
    score += weights["debt"] * normalize_debt(total_debt)
    score += weights["average_monthly_revenue"] * normalize_revenue(monthly_revenue)
    score += weights["past_due_amount"] * (
        1
        if user.get("max_past_due_amount", 0) == 0
        or user.get("max_past_due_amount", 0) < monthly_revenue
        else 0.4
    )
    score += weights["overdue_installments"] * normalize_overdue_installments(
        user.get("num_overdue_installments", 0)
    )
    score += weights["open_contract"] * normalize_open_contracts(
        user.get("total_open_contracts", 0)
    )
    score += weights["past_due_days"] * calculate_past_due_days_score(
        user.get("max_past_due_days", 0)
    )
    score += weights["debt_to_income_ratio"] * normalize_debt_to_income_ratio(
        calculate_debt_to_income_ratio(monthly_income, total_debt)[0]
    )

    return score


def calculate_middle_features(user):
    # Weights assigned to middle impact features
    weights = {
        "business_duration": 0.30,
        "payment_methods": 0.25,
        "age": 0.25,
        "dependants": 0.20,
    }

    # Calculate the middle feature score
    score = 0
    score += weights["business_duration"] * normalize_business_duration(
        user.get("months_in_business", 0)
    )
    score += weights["payment_methods"] * normalize_payment_methods(
        user.get("payment_methods", [])
    )
    score += weights["age"] * normalize_age(user.get("age", 0))
    score += weights["dependants"] * normalize_dependants(user.get("num_dependants", 0))

    return score


def calculate_low_features(user):
    # Weights assigned to low impact features
    weights = {"credit_inquiries": 0.40, "regional_gdp": 0.30, "housing_status": 0.30}

    # Calculate the low feature score
    score = 0
    score += weights["credit_inquiries"] * normalize_credit_inquiries(
        user.get("num_credit_inquiries", 0)
    )
    score += weights["regional_gdp"] * normalize_rgp(
        user.get("region_gdp", 0), user.get("national_average_gdp", 1)
    )
    score += weights["housing_status"] * normalize_housing_status(
        user.get("housing_status", "")
    )

    return score


def calculate_debt_to_revenue_ratio(total_debt, monthly_revenue):
    # Calculate the ratio of total debt to monthly revenue
    if monthly_revenue == 0:
        return 1  # Default to maximum ratio if revenue is 0 to avoid division by zero
    return total_debt / monthly_revenue
    

