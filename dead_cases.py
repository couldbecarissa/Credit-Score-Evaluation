import numpy as np
import normalization
import credit_risk_evaluation
from credit_risk_evaluation import MaturityIndex,CreditAccounts

user={

}

# Define weights for each factor
weights = {
        'lack_financial_documentation': 0.10,
        'negative_credit_history': 0.10*CreditAccounts(num_credit_accounts=user.get("num_credit_accounts",0),
                                                       total_open_contracts=user.get("total_open_contracts",0)),
        'fraud_or_dishonesty': 0.15,
        'high_debt_to_income_ratio': 0.08,
        'business_instability': 0.08,
        'lack_collateral': 0.12 if normalization.is_collateral==True else 0,
        'ineligible_business_type': 0.06,
        'high_risk_location': 0.05*normalization.normalize_rgp(B5=user.get("B5",0)),
        'legal_issues': 0.07,
        'inadequate_management_experience': 0.15*MaturityIndex(age=user.get("age",0),years_in_business=user.get("C6",0)),
        'inconsistent_loan_purpose': 0.04,
    }

def is_dead(user):
    # Calculate weighted risk score
    risk_score = sum(weights['high_risk_location'],
                     weights['inadequate_management_experience'],
                     weights['negative_credit_history'],
                     weights['lack_collateral'])
    
    # Normalize risk score to ensure it's between 0 and 1
    norm= min(max(risk_score, 0), 1)
    if(norm<0.75):
        print("You are not eligible for a loan.")
    else:print("You are on rocky ground,Sir.")




