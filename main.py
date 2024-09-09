import numpy as np
import credit_risk_evaluation
import scalability
import dead_cases

# Sample users
user={
        "financial_literacy":"yes",
        "total_amount_in_debt":49750,
        "customer_payment_method":"cash",
        "housing_situation":3,
        "own_vs_rent":"own",
        "emergency_handling":"dip into savings",
        "age":32,
        "years_in_business":8,
        "monthly_demo_affordability":70000,
        "num_overdue_installments":2,
        "num_credit_inquiries":6,
        "max_past_due_amount":60000,
        "max_past_due_days":100,
        "loan_term":"a week",
       " num_credit_accounts":3,
        "total_open_contracts" :4, 
        "loan_interest_rate":10,
        "household_region":"morogoro" 
    }

credit_score_user=credit_risk_evaluation.should_calculate(user=user)
scaled_credit=scalability.ScaledPaymentHistory(max_past_due_days=user.get("max_past_due_days", 0),
                                      max_past_due_amount=user.get("max_past_due_amount", 0),
                                      total_amount_in_debt=user.get("total_amount_in_debt", 0),
                                      num_overdue_installments= user.get("num_credit_inquiries", 0),
                                      monthly_demo_affordability=user.get("monthly_demo_affordability", 0)
                                      )
#I will write another function to determine whether of not the credit score should be scaled
scaled_credit_score_user=(credit_score_user*scaled_credit)/(credit_score_user+scaled_credit)

print(f"User Credit Score: {credit_score_user:,} creds")
print(f"User Scaled Credit Score: {scaled_credit_score_user:,} creds")

loan_given=np.round(credit_risk_evaluation.approve_loan(credit_score=credit_score_user))
print(loan_given)