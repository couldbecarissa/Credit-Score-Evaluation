import numpy as np
import credit_risk_evaluation


# Sample users
user1={
        "financial_literacy":"yes",
        "total_amount_in_debt":1000000,
        "C7":"cash",
        "B15":3,
        "C3":"own",
        "age":32,
        "C6":4,#
        "monthly_demo_affordability":70000,
        "num_overdue_installments":5,#
        "num_credit_inquiries":6,
        "max_past_due_amount":60000,
        "max_past_due_days":1,
       "num_credit_accounts":7,
        "total_open_contracts":6, 
        "B5":"Mbeya",#
        "loan_term":15
    }

credit_score_user=credit_risk_evaluation.should_calculate(user=user1)

print(f"User Credit Score: {np.round(credit_score_user,decimals=3):,} creds")

loan_given=np.round(credit_risk_evaluation.approve_loan(credit_score=credit_score_user),decimals=0)
print(loan_given)