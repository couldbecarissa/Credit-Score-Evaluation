
def normalize_debt_to_income_ratio(ratio):
    # Normalize the debt-to-income ratio
    if ratio <= 0.3:
        return 1.0
    elif ratio <= 0.5:
        return 0.8
    elif ratio <= 0.7:
        return 0.6
    elif ratio <= 1.0:
        return 0.4
    elif ratio <= 1.5:
        return 0.2
    else:
        return 0.0


def calculate_debt_to_income_ratio(monthly_income, total_debt, estimated_loan_term=12):
    # Calculate the debt-to-income ratio
    if monthly_income == 0:
        return 0, False
    
    estimated_monthly_debt = total_debt / estimated_loan_term
    
    ratio = estimated_monthly_debt / monthly_income
    is_eligible = ratio <= 1.5
    return min(ratio, 2), is_eligible


def normalize_business_duration(months_in_business):
    # Normalize the duration of business operations
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
    # Normalize the available payment methods
    score = 0
    if 'cash' in methods:
        score += 0.3
    if 'mobile_money' in methods:
        score += 0.5
    if 'bank' in methods:
        score += 0.7
    return min(score, 1.0)


def normalize_age(age):
    # Normalize age for scoring purposes
    if age < 25:
        return 0.3
    elif age < 35:
        return 0.6
    elif age < 50:
        return 1.0
    else:
        return 0.8


def normalize_revenue(monthly_revenue):
    # Normalize the monthly revenue
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
    # Normalize the number of dependants
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
    # Normalize the debt amount
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


def normalize_overdue_installments(num_overdue_installments):
    # Normalize the number of overdue installments
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
    # Normalize the number of credit inquiries
    if num_credit_inquiries == 0:
        return 1.0
    elif num_credit_inquiries == 1:
        return 0.8
    elif num_credit_inquiries == 2:
        return 0.6
    elif num_credit_inquiries == 3:
        return 0.4
    elif num_credit_inquiries == 4:
        return 0.2
    else:
        return 0.0


def normalize_open_contracts(total_open_contracts):
    # Normalize the number of open contracts
    if total_open_contracts == 0:
        return 1.0
    elif total_open_contracts == 1:
        return 0.8
    elif total_open_contracts == 2:
        return 0.6
    elif total_open_contracts == 3:
        return 0.4
    elif total_open_contracts == 4:
        return 0.2
    else:
        return 0.0


def normalize_rgp(region_gdp, national_average_gdp):
    # Normalize the Regional GDP relative to the National Average GDP
    ratio = region_gdp / national_average_gdp
    if ratio >= 1.2:
        return 1.0
    elif ratio >= 1.0:
        return 0.8
    elif ratio >= 0.8:
        return 0.6
    elif ratio >= 0.6:
        return 0.4
    elif ratio >= 0.4:
        return 0.2
    else:
        return 0.0


def normalize_housing_status(housing_status):
    # Normalize housing status
    if housing_status == "owned":
        return 1.0
    elif housing_status == "mortgaged":
        return 0.8
    elif housing_status == "rented":
        return 0.6
    elif housing_status == "other":
        return 0.4
    else:
        return 0.2


def calculate_past_due_days_score(past_due_days):
    # Normalize past due days for scoring
    if past_due_days <= 7:
        return 1.0
    elif past_due_days <= 14:
        return 0.8
    elif past_due_days <= 21:
        return 0.6
    elif past_due_days <= 28:
        return 0.4
    elif past_due_days <= 35:
        return 0.2
    else:
        return 0.0