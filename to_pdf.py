from fpdf import FPDF

# Create a new instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Add DejaVu font (regular and bold)
pdf.add_font("DejaVu", "", "./dejavu-sans/ttf/DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "./dejavu-sans/ttf/DejaVuSans-Bold.ttf", uni=True)

# Set the font for title
pdf.set_font('DejaVu', 'B', 16)
pdf.cell(200, 10, txt='Formula Breakdown (Credit Score Calculation)', new_x='LMARGIN', new_y='NEXT', align='C')

# Set font for content
pdf.set_font('DejaVu', '', 12)

# Revised content
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
"""

# Add each line to the PDF
for line in formatted_content.split('\n'):
    pdf.cell(200, 10, txt=line, new_x='LMARGIN', new_y='NEXT')

# Save to a new file
formatted_output_file = "credit_score.pdf"
pdf.output(formatted_output_file)

print("PDF saved as:", formatted_output_file)
