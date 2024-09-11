import numpy as np
import credit_risk_evaluation
import dead_cases

# Sample users
user1={
        "financial_literacy":"yes",
        "total_amount_in_debt":490000,
        "C7":"cash",
        "B15":3,
        "C3":"rent",
        "age":32,
        "C6":8,
        "monthly_demo_affordability":7000,
        "num_overdue_installments":9,
        "num_credit_inquiries":2,
        "max_past_due_amount":60000,
        "max_past_due_days":1,
       " num_credit_accounts":6,
        "total_open_contracts" :1, 
        "B5":"Morogoro" ,
        "loan_term":7
    }

credit_score_user=credit_risk_evaluation.should_calculate(user=user1)

print(f"User Credit Score: {np.round(credit_score_user,decimals=3):,} creds")

loan_given=np.round(credit_risk_evaluation.approve_loan(credit_score=credit_score_user))
print(loan_given)