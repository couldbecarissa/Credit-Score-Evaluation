import numpy as np
import credit_risk_evaluation
import dead_cases

# Sample users
user1={
        "financial_literacy":"yes",
        "total_amount_in_debt":49750,
        "C7":"cash",
        "B15":3,
        "C3":"rent",
        "age":32,
        "C6":8,
        "monthly_demo_affordability":70000,
        "num_overdue_installments":2,
        "num_credit_inquiries":6,
        "max_past_due_amount":60000,
        "max_past_due_days":100,
        "loan_term":"a week",
       " num_credit_accounts":3,
        "total_open_contracts" :4, 
        "loan_interest_rate":10,
        "B5":"morogoro" ,
        "loan_term":9
    }

credit_score_user=credit_risk_evaluation.should_calculate(user=user1)

print(f"User Credit Score: {np.round(credit_score_user,decimals=3):,} creds")

loan_given=np.round(credit_risk_evaluation.approve_loan(credit_score=credit_score_user))
print(loan_given)