import sqlite3
import pandas as pd

# Step 1: Connect to SQLite database
conn = sqlite3.connect('data.db')  # Replace with your database name

# Step 2: Query the database table
table_name = 'kuza_users'  # Replace with your table name
query = f'SELECT * FROM {table_name}'
df = pd.read_sql_query(query, conn)

# Step 3: Export the DataFrame to a CSV file
csv_file_path = 'data.csv'  # Replace with your desired CSV file path
df.to_csv(csv_file_path, index=False)

# Step 4: Close the database connection
conn.close()

print("Data exported to CSV successfully!")
