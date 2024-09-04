# Importing necessary libraries
import pandas as pd
import numpy as np
import sys, random

n_samples = 500

# Initialize a list to store the DataFrames
dfs = []

# Print progress message before starting the loop
print("Generating random data...")

# Iterate n_samples times
for d in range(n_samples):
    # Print progress message within the loop
    print(f"Processing sample {d+1}/{n_samples}")

    # Generate random data for each column
    gender = np.random.choice(["male", "female"], n_samples)
    age = np.random.randint(20, 60, n_samples)
    extra_info = np.random.choice(["0.2", "0.4", "0.6", "0.8", "1"], n_samples)
    housing_situation = np.random.randint(1, 10, n_samples)
    own_vs_rent = np.random.choice(["own", "rent"], n_samples)
    years_in_business = np.random.randint(0, 20, n_samples)
    customer_payment_method = np.random.choice(["cash", "mobile money", "bank payment", "loan", "other"], n_samples)
    emergency_handling = np.random.choice(["dip into savings", "loan more money"], n_samples)
    financial_literacy = np.random.choice(["yes", "no"], n_samples)
    inquiriesOverLast12Months = np.random.randint(0, 10, n_samples)
    total_amount_in_debt = np.random.randint(50000, 500000, n_samples)
    periodicityOfPayments = np.random.choice(["monthly", "quarterly", "semi annually", "annually"], n_samples)
    numberOfOverdueInstallments = np.random.randint(0, 10, n_samples)
    mainChallenges = np.random.choice(["credit and financing", "inventory management", "supply chain issues", "other"], n_samples)
    supportType = np.random.choice(["financial assistance", "business training", "infrastructure improvements"], n_samples)
    

    # Create a DataFrame for the current sample
    columns = ['gender', 'age', 'extra_info', 'housing_situation', 'own_vs_rent',
               'years_in_business', 'customer_payment_method',
               'emergency_handling', 'financial_literacy',
               'inquiriesOverLast12Months', 'total_amount_in_debt',
               'periodicityOfPayments', 'numberOfOverdueInstallments',
               'mainChallenges', 'supportType']

    row = {'gender': gender,
           'age': age,
           'extra_info': extra_info,
           'housing_situation': housing_situation,
           'own_vs_rent': own_vs_rent,
           'years_in_business': years_in_business,
           'customer_payment_method': customer_payment_method,
           'emergency_handling': emergency_handling,
           'financial_literacy': financial_literacy,
           'inquiriesOverLast12Months': inquiriesOverLast12Months,
           'total_amount_in_debt': total_amount_in_debt,
           'periodicityOfPayments': periodicityOfPayments,
           'numberOfOverdueInstallments': numberOfOverdueInstallments,
           'mainChallenges': mainChallenges,
           'supportType': supportType}

    df = pd.DataFrame(row, columns=columns)

    # Append the DataFrame to the list
    dfs.append(df)

# Save the final DataFrame to a CSV file
df.to_csv('data2.csv', index=False)

print("Data generation and saving completed.")
