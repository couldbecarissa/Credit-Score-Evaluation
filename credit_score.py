import numpy as np


def calculate_credit_score(
    age,
    income,
    debt,
    credit_history,
    dependents,
    household_size,
    time_in_business,
    inquiries_last_12_months,
    overdue_installments,
    loan_amount,
):
    # Adjust weights dynamically based on conditions (e.g., local economic factors)
    income_weight = 0.25 if income > 500000 else 0.3
    debt_weight = 0.15 if debt < 200000 else 0.2
    credit_history_weight = 0.2
    dependents_weight = 0.05
    household_size_weight = 0.05
    time_in_business_weight = 0.1
    inquiries_weight = 0.05
    overdue_installments_weight = 0.05
    loan_amount_weight = 0.1

    # Normalize the age to a value for calculation (using 18-65 as typical working age range)
    normalized_age = (min(65, max(18, age)) - 18) / (65 - 18)

    # Normalize other inputs using adjusted methods
    normalized_income = np.log1p(income) / np.log(2000001)
    normalized_debt = np.sqrt(debt) / np.sqrt(1000000)
    normalized_credit_history = min(10, credit_history) / 10
    normalized_loan_amount = np.sqrt(loan_amount) / np.sqrt(500000)

    # Adjust for additional factors
    normalized_dependents = min(10, dependents) / 10
    household_size_map = {1: 1.1, 2: 1.0, 3: 0.9, 4: 0.8, 5: 0.7}
    household_size_value = household_size_map.get(household_size, 0.9)
    time_in_business_map = {
        "less than 1 year": 0.6,
        "1-3": 0.8,
        "3-5": 1.0,
        "5-10": 1.2,
        "more than 10": 1.3,
    }
    time_in_business_value = time_in_business_map.get(time_in_business, 1.0)
    normalized_inquiries = min(10, inquiries_last_12_months) / 10
    normalized_overdue_installments = min(10, overdue_installments) / 10

    # Calculate the weighted sum
    weighted_sum = (
        (normalized_age * 0.1)
        + (normalized_income * income_weight)
        - (normalized_debt * debt_weight)
        + (normalized_credit_history * credit_history_weight)
        + (normalized_dependents * dependents_weight)
        + (household_size_value * household_size_weight)
        + (time_in_business_value * time_in_business_weight)
        - (normalized_inquiries * inquiries_weight)
        - (normalized_overdue_installments * overdue_installments_weight)
        + (normalized_loan_amount * loan_amount_weight)
    )

    # Map the weighted sum to a credit score scale
    min_score = 0
    max_score = 500000
    credit_score = max(
        min_score,
        min(
            max_score,
            min_score
            + (max_score - min_score)
            * (
                weighted_sum
                / (
                    0.1
                    + income_weight
                    + debt_weight
                    + credit_history_weight
                    + dependents_weight
                    + household_size_weight
                    + time_in_business_weight
                    + inquiries_weight
                    + overdue_installments_weight
                    + loan_amount_weight
                )
            ),
        ),
    )

    return credit_score


# Sample users
users = [
    {
        "age": 50,
        "income": 600000,
        "debt": 100000,
        "credit_history": 1,
        "dependents": 0,
        "household_size": 1,
        "time_in_business": "less than 1 year",
        "inquiries_last_12_months": 5,
        "overdue_installments": 2,
        "loan_amount": 50000,
    },
    {
        "age": 28,
        "income": 800000,
        "debt": 50000,
        "credit_history": 3,
        "dependents": 1,
        "household_size": 2,
        "time_in_business": "5-10",
        "inquiries_last_12_months": 1,
        "overdue_installments": 0,
        "loan_amount": 100000,
    },
    {
        "age": 40,
        "income": 1200000,
        "debt": 200000,
        "credit_history": 10,
        "dependents": 2,
        "household_size": 2,
        "time_in_business": "more than 10",
        "inquiries_last_12_months": 3,
        "overdue_installments": 1,
        "loan_amount": 200000,
    },
    {
        "age": 32,
        "income": 700000,
        "debt": 150000,
        "credit_history": 5,
        "dependents": 0,
        "household_size": 1,
        "time_in_business": "3-5",
        "inquiries_last_12_months": 4,
        "overdue_installments": 3,
        "loan_amount": 150000,
    },
    {
        "age": 45,
        "income": 1000000,
        "debt": 100000,
        "credit_history": 8,
        "dependents": 3,
        "household_size": 3,
        "time_in_business": "more than 10",
        "inquiries_last_12_months": 2,
        "overdue_installments": 0,
        "loan_amount": 250000,
    },
    {
        "age": 23,
        "income": 500000,
        "debt": 200000,
        "credit_history": 0,
        "dependents": 0,
        "household_size": 1,
        "time_in_business": "1-3",
        "inquiries_last_12_months": 7,
        "overdue_installments": 4,
        "loan_amount": 80000,
    },
    {
        "age": 30,
        "income": 750000,
        "debt": 120000,
        "credit_history": 4,
        "dependents": 1,
        "household_size": 2,
        "time_in_business": "5-10",
        "inquiries_last_12_months": 2,
        "overdue_installments": 1,
        "loan_amount": 120000,
    },
    {
        "age": 37,
        "income": 1100000,
        "debt": 180000,
        "credit_history": 6,
        "dependents": 2,
        "household_size": 3,
        "time_in_business": "3-5",
        "inquiries_last_12_months": 3,
        "overdue_installments": 2,
        "loan_amount": 180000,
    },
    {
        "age": 22,
        "income": 550000,
        "debt": 150000,
        "credit_history": 1,
        "dependents": 0,
        "household_size": 1,
        "time_in_business": "less than 1 year",
        "inquiries_last_12_months": 6,
        "overdue_installments": 3,
        "loan_amount": 70000,
    },
    {
        "age": 29,
        "income": 850000,
        "debt": 80000,
        "credit_history": 5,
        "dependents": 1,
        "household_size": 2,
        "time_in_business": "1-3",
        "inquiries_last_12_months": 2,
        "overdue_installments": 0,
        "loan_amount": 90000,
    },
]

# Calculate and print credit scores for each user
for i, user in enumerate(users):
    credit_score = calculate_credit_score(
        user["age"],
        user["income"],
        user["debt"],
        user["credit_history"],
        user["dependents"],
        user["household_size"],
        user["time_in_business"],
        user["inquiries_last_12_months"],
        user["overdue_installments"],
        user["loan_amount"],
    )
    print(f"User {i + 1} Credit Score: {credit_score:,} TSH")
