# Importing necessary libraries
import pandas as pd
import numpy as np
import sys, random

n_samples = 20

# Initialize a list to store the DataFrames
dfs = []

# Print progress message before starting the loop
print("Generating random data...")

# Iterate n_samples times
for d in range(n_samples):
    # Print progress message within the loop
    print(f"Processing sample {d+1}/{n_samples}")

    # Generate random data for each column
    age = np.random.randint(20, 60, n_samples)
    housing_situation = np.random.randint(1, 10, n_samples)
    own_vs_rent = np.random.choice(["own", "rent"], n_samples)
    years_in_business = np.random.randint(0, 20, n_samples)
    customer_payment_method = np.random.choice(["cash", "mobile money", "bank payment", "loan", "other"], n_samples)
    emergency_handling = np.random.choice(["dip into savings", "loan more money"], n_samples)
    financial_literacy = np.random.choice(["yes", "no"], n_samples)
    num_credit_inquiries = np.random.randint(0, 10, n_samples)
    total_amount_in_debt = np.random.randint(50000, 500000, n_samples)
    loan_term = np.random.choice(["one week", "two weeks","a month"], n_samples)
    num_overdue_installments = np.random.randint(0, 10, n_samples)
    monthly_demo_affordability=np.random.randint(20000,1000000,n_samples)
    max_past_due_amount=np.random.randint(20000,1000000,n_samples)
    max_past_due_days=np.random.randint(0,11,n_samples)
    num_credit_accounts=np.random.randint(0,20,n_samples)
    total_open_contracts=np.random.randint(0,20,n_samples)

    # Create a DataFrame for the current sample
    columns = ['gender', 'age', 'extra_info', 'housing_situation', 'own_vs_rent',
               'years_in_business', 'customer_payment_method',
               'emergency_handling', 'financial_literacy',
               'num_credit_inquiries', 'total_amount_in_debt',
               'loan_term', 'num_overdue_installments','monthly_demo_affordability',
               'max_past_due_amount','max_past_due_days',
               'num_credit_accounts','total_open_contracts'
            ]

    row = {
           'age': age,
           'housing_situation': housing_situation,
           'own_vs_rent': own_vs_rent,
           'years_in_business': years_in_business,
           'customer_payment_method': customer_payment_method,
           'emergency_handling': emergency_handling,
           'financial_literacy': financial_literacy,
           'num_credit_inquiries': num_credit_inquiries,
           'total_amount_in_debt': total_amount_in_debt,
           'loan_term': loan_term,
           'monthly_demo_affordability':monthly_demo_affordability,
           'max_past_due_amount':max_past_due_amount,
           'max_past_due_days':max_past_due_days,
           'num_overdue_installments': num_overdue_installments,
           'num_credit_accounts':num_credit_accounts,
           'total_open_contracts':total_open_contracts}

    df = pd.DataFrame(row, columns=columns)

    # Append the DataFrame to the list
    dfs.append(df)

# Save the final DataFrame to a CSV file
df.to_csv('data2.csv', index=False)

print("Data generation and saving completed.")
