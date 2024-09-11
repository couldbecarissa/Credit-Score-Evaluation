import numpy as np

def normalize_business_duration(months_in_business):
    """
    Normalize business duration, giving higher scores to businesses operating longer.
    """
    if months_in_business < 6:
        return 0.2
    elif months_in_business < 12:
        return 0.4
    elif months_in_business < 24:
        return 0.6
    elif months_in_business < 36:
        return 0.8
    else:
        return 1.0

def normalize_payment_methods(methods):
    """
    Normalize payment methods, favoring more formal methods.
    """
    score = 0
    if 'cash' in methods:
        score += 0.3
    if 'mobile_money' in methods:
        score += 0.5
    if 'bank' in methods:
        score += 0.7
    return min(score, 1.0)

def normalize_age(age):
    """
    Normalize age, favoring middle-aged applicants.
    """
    if age < 25:
        return 0.3
    elif age < 35:
        return 0.6
    elif age < 50:
        return 1.0
    else:
        return 0.8

def normalize_revenue(monthly_revenue):
    """
    Normalize monthly revenue on a scale suitable for market sellers.
    """
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
    """
    Normalize number of dependants, considering typical family sizes in Tanzania.
    """
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
    """
    Normalize debt based on the loan range of 50,000 to 500,000 TSh.
    """
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
    """
    Calculate debt-to-income ratio using total debt and estimating monthly payments.
    
    :param monthly_income: User's monthly income
    :param total_debt: User's total debt
    :param estimated_loan_term: Estimated loan term in months (default 12)
    :return: Tuple of (debt_to_income_ratio, is_eligible)
    """
    if monthly_income == 0:
        return 0, False
    
    # Estimate monthly debt payment
    estimated_monthly_debt = total_debt / estimated_loan_term
    
    ratio = estimated_monthly_debt / monthly_income
    is_eligible = ratio <= 1.5
    return min(ratio, 2), is_eligible

def normalize_overdue_installments(num_overdue_installments):
    """
    Normalize number of overdue installments, being stricter for market sellers.
    """
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
    """
    Normalize number of credit inquiries, considering limited credit access.
    """
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
    """
    Normalize regional GDP per capita against national average.
    """
    ratio = region_gdp / national_average_gdp
    return min(max(ratio, 0), 1)  # Ensure the result is between 0 and 1

def is_empty(field):
    """
    Check if a field is empty or None.
    """
    return field is None or field == ""