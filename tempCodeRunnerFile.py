from fpdf import FPDF
# Create a new instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set title
pdf.set_font('Arial', 'B', 16)
pdf.cell(200, 10, txt='Formula Breakdown (Credit Score Calculation)', ln=True, align='C')

# Set font for content
pdf.set_font('Arial', '', 12)

# Revised content without markdown symbols
formatted_content = """
Formula Breakdown (Credit Score Calculation)

1. High-Impact Factors (70% of total score):
   - Debt: If the user has less debt, they get a higher score.
   - Monthly Income: More income means a higher score.
   - Past Due Payments: If they missed payments, the score is lowered.
   - Overdue Installments: More overdue installments decrease the score.
   - Open Contracts: Fewer open financial obligations increase the score.
   - Days Past Due: Fewer late days on payments give a better score.
   - Debt-to-Income Ratio: A lower ratio (more income compared to debt) gives a better score.

2. Medium-Impact Factors (20% of total score):
   - Business Duration: The longer the business has been running, the higher the score.
   - Payment Methods: Having more ways to pay (cash, bank, mobile money) increases the score.
   - Age: Middle-aged people (25-50 years) score higher than very young or old people.
   - Dependents: Fewer dependents means a higher score.

3. Low-Impact Factors (10% of total score):
   - Credit Inquiries: Fewer credit checks give a higher score.
   - Regional Economy: If the person lives in a wealthier region, they get a higher score.
   - Housing Status: Owning a home scores the highest, renting scores lower.

4. Final Calculation:
   - Combine all factors using their respective weights to get a final score.
   - Note: If the person has a debt-to-income ratio of 0.8 or higher, their score will be 0, disqualifying them from a loan.

Loan Calculation Formula:
- If the monthly income is greater than or equal to 500,000 TSH, the user can get a loan of 500,000 TSH.
- If the monthly income is less than 500,000 TSH, the loan amount will be equal to the income.

Credit Score Calculation:
High-Impact Factors (70% of total score):
- Debt: Debt Score = W_debt × Normalize_Debt(total_amount_in_debt)
- Monthly Revenue: Revenue Score = W_revenue × Normalize_Revenue(average_monthly_revenue)
- Past Due Amount: Past Due Score = W_past_due × Score_Past_Due_Amount(max_past_due_amount)
- Overdue Installments: Overdue Installments Score = W_overdue_installments × Normalize_Overdue_Installments(num_overdue_installments)
- Open Contracts: Open Contracts Score = W_open_contracts × Normalize_Open_Contracts(total_open_contracts)
- Past Due Days: Past Due Days Score = W_past_due_days × Calculate_Past_Due_Days_Score(max_past_due_days)
- Debt-to-Income Ratio: Debt-to-Income Ratio Score = W_debt_to_income × Normalize_Debt_To_Income_Ratio(Debt-to-Income Ratio)
  Where:
    - W_debt = 0.30
    - W_revenue = 0.30
    - W_past_due = 0.10
    - W_overdue_installments = 0.10
    - W_open_contracts = 0.05
    - W_past_due_days = 0.05
    - W_debt_to_income = 0.10

Middle-Impact Factors (20% of total score):
- Business Duration: Business Duration Score = W_business_duration × Normalize_Business_Duration(months_in_business)
- Payment Methods: Payment Methods Score = W_payment_methods × Normalize_Payment_Methods(payment_methods)
- Age: Age Score = W_age × Normalize_Age(age)
- Dependents: Dependents Score = W_dependants × Normalize_Dependants(num_dependants)
  Where:
    - W_business_duration = 0.30
    - W_payment_methods = 0.25
    - W_age = 0.25
    - W_dependants = 0.20

Low-Impact Factors (10% of total score):
- Credit Inquiries: Credit Inquiries Score = W_credit_inquiries × Normalize_Credit_Inquiries(num_credit_inquiries)
- Regional GDP: Regional GDP Score = W_regional_gdp × Normalize_RGP(region_gdp, national_average_gdp)
- Housing Status: Housing Status Score = W_housing_status × Normalize_Housing_Status(housing_status)
  Where:
    - W_credit_inquiries = 0.40
    - W_regional_gdp = 0.30
    - W_housing_status = 0.30

Overall Credit Score Calculation:
Credit Score = (0.70 × High-Impact Score) + (0.20 × Middle-Impact Score) + (0.10 × Low-Impact Score)

Loan Amount Calculation:
- If Monthly Revenue ≥ 500,000 TSH:
  Approved Loan = 500,000 TSH
- If Monthly Revenue < 500,000 TSH:
  Approved Loan = average_monthly_revenue
"""

# Adding each line to the PDF without markdown formatting
for line in formatted_content.split('\n'):
    pdf.cell(200, 10, txt=line, ln=True)

# Save to a new file
formatted_output_file = "/mnt/data/credit_score_formatted.pdf"
pdf.output(formatted_output_file)

formatted_output_file
