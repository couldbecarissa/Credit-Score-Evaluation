import pandas as pd

# Function to load user data from CSV file
def load_user_data_from_csv(file_path):
    """
    Load user data from a CSV file into a pandas DataFrame.
    Each row in the CSV represents a user.
    """
    return pd.read_csv(file_path)

# Function to calculate credit scores for multiple users
def calculate_credit_scores(df):
    """
    Calculate credit scores for users in the pandas DataFrame.
    Returns a dictionary of user IDs and their respective credit scores.
    """
    scores = {}
    
    # Iterate over each row (user data)
    for _, row in df.iterrows():
        user_data = row.to_dict()  # Convert the row to a dictionary
        user_id = user_data.get('ID')  # Get the user ID
        score = calculate_credit_score(user_data)  # Calculate the score for this user
        scores[user_id] = score  # Store the score with the user ID as the key
    
    return scores

# Function to calculate credit score for a single user
def calculate_credit_score(user_data):
    """
    Calculate the credit score based on user data.
    The score is based on the FICO model but customized for sokoni context.
    """

    # Initialize base score
    score = 300

    # Payment History (35% of FICO Score)
    payment_history_score = calculate_payment_history(user_data)
    score += payment_history_score * 0.35

    # Amounts Owed (30% of FICO Score)
    amounts_owed_score = calculate_amounts_owed(user_data)
    score += amounts_owed_score * 0.30

    # Length of Credit History (15% of FICO Score)
    length_of_credit_score = calculate_length_of_credit(user_data)
    score += length_of_credit_score * 0.15

    # Credit Mix (10% of FICO Score)
    credit_mix_score = calculate_credit_mix(user_data)
    score += credit_mix_score * 0.10

    # New Credit (10% of FICO Score)
    new_credit_score = calculate_new_credit(user_data)
    score += new_credit_score * 0.10

    # Ensure the score is within the valid range
    return min(max(int(score), 300), 850)

# Supporting functions for different aspects of credit score calculation
def calculate_payment_history(user_data):
    score = 0
    if safe_int(user_data.get('E8')) == 1:
        score += 50
    if safe_int(user_data.get('E9')) == 1:
        score += 100

    missed_payments = safe_int(user_data.get('missed_payments', 0))
    if missed_payments > 0:
        score -= min(missed_payments * 10, 50)

    return score

def calculate_amounts_owed(user_data):
    score = 0
    monthly_revenue = safe_float(user_data.get('D8', '0'))
    monthly_savings = safe_float(user_data.get('E3', '0'))

    if monthly_revenue > 0:
        debt_to_income = 1 - (monthly_savings / monthly_revenue)
        if debt_to_income <= 0.3:
            score += 100
        elif debt_to_income <= 0.5:
            score += 75
        elif debt_to_income <= 0.7:
            score += 50
        else:
            score += 25
    return score

def calculate_length_of_credit(user_data):
    score = 0
    business_duration = user_data.get('C6', '')
    if isinstance(business_duration, str):
        if 'Less than 1 year' in business_duration:
            score += 20
        elif any(year in business_duration for year in ['1-2', '3-5']):
            score += 60
        else:
            score += 100
    return score

def calculate_credit_mix(user_data):
    score = 0
    financial_services = sum([safe_int(user_data.get(f'E7_{i}', 0)) for i in range(1, 13)])

    if financial_services >= 3:
        score += 100
    elif financial_services >= 2:
        score += 75
    elif financial_services >= 1:
        score += 50

    return score

def calculate_new_credit(user_data):
    score = 100
    if safe_int(user_data.get('E18')) == 1:
        score -= 50
    return score

# Utility functions for safely converting types
def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

# Function to explain the score rating
def explain_score(score):
    if score >= 800:
        return "Exceptional"
    elif score >= 740:
        return "Very Good"
    elif score >= 670:
        return "Good"
    elif score >= 580:
        return "Fair"
    else:
        return "Poor"

# Function to calculate loan amount based on credit score
def calculate_loan_amount(score):
    """
    Calculate the loan amount based on the credit score.
    The score is scaled from 0 to 500,000 TSH.
    """
    min_score = 300
    max_score = 850
    min_loan = 0
    max_loan = 500000

    # Scale the score to the loan amount
    if score < min_score:
        return min_loan
    elif score > max_score:
        return max_loan
    else:
        return min_loan + ((score - min_score) / (max_score - min_score)) * (max_loan - min_loan)

# Example usage
file_path = 'data.csv'  # Replace with your actual CSV file path

# Load user data from the CSV file
df_users = load_user_data_from_csv(file_path)

# Calculate credit scores for all users
credit_scores = calculate_credit_scores(df_users)

# Calculate and print loan amounts for all users
for user_id, score in credit_scores.items():
    loan_amount = calculate_loan_amount(score)
    print(f"User ID: {user_id}, Credit Score: {score}")
    print(f"Credit Rating: {explain_score(score)}")
    print(f"Loan Amount: {loan_amount} TSH")
    print()
