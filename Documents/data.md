

### **High-Impact Factors (70% of total score)**:

1. **Debt**:  
   Debt Score = W_debt × Normalize_Debt(total_amount_in_debt)  
   Where W_debt = 0.30

2. **Monthly Revenue**:  
   Revenue Score = W_revenue × Normalize_Revenue(average_monthly_revenue)  
   Where W_revenue = 0.30

3. **Past Due Amount**:  
   Past Due Score = W_past_due × Score_Past_Due_Amount(max_past_due_amount)  
   Where W_past_due = 0.10

4. **Overdue Installments**:  
   Overdue Installments Score = W_overdue_installments × Normalize_Overdue_Installments(num_overdue_installments)  
   Where W_overdue_installments = 0.10

5. **Open Contracts**:  
   Open Contracts Score = W_open_contracts × Normalize_Open_Contracts(total_open_contracts)  
   Where W_open_contracts = 0.05

6. **Past Due Days**:  
   Past Due Days Score = W_past_due_days × Calculate_Past_Due_Days_Score(max_past_due_days)  
   Where W_past_due_days = 0.05

7. **Debt-to-Income Ratio**:  
   Debt-to-Income Ratio Score = W_debt_to_income × Normalize_Debt_To_Income_Ratio(debt_to_income_ratio)  
   Where W_debt_to_income = 0.10

---

### **Middle-Impact Factors (20% of total score)**:

1. **Business Duration**:  
   Business Duration Score = W_business_duration × Normalize_Business_Duration(months_in_business)  
   Where W_business_duration = 0.30

2. **Payment Methods**:  
   Payment Methods Score = W_payment_methods × Normalize_Payment_Methods(payment_methods)  
   Where W_payment_methods = 0.25

3. **Age**:  
   Age Score = W_age × Normalize_Age(age)  
   Where W_age = 0.25

4. **Dependents**:  
   Dependents Score = W_dependants × Normalize_Dependants(num_dependants)  
   Where W_dependants = 0.20

---

### **Low-Impact Factors (10% of total score)**:

1. **Credit Inquiries**:  
   Credit Inquiries Score = W_credit_inquiries × Normalize_Credit_Inquiries(num_credit_inquiries)  
   Where W_credit_inquiries = 0.40

2. **Regional GDP**:  
   Regional GDP Score = W_regional_gdp × Normalize_RGP(region_gdp, national_average_gdp)  
   Where W_regional_gdp = 0.30

3. **Housing Status**:  
   Housing Status Score = W_housing_status × Normalize_Housing_Status(housing_status)  
   Where W_housing_status = 0.30

---

### **Overall Credit Score Calculation**:

Credit Score = (0.70 × High-Impact Score) + (0.20 × Middle-Impact Score) + (0.10 × Low-Impact Score)

---

### **Loan Amount Calculation**:

- If **Monthly Revenue ≥ 500,000 TSH**: Approved Loan = 500,000 TSH  
- If **Monthly Revenue < 500,000 TSH**: Approved Loan = average_monthly_revenue