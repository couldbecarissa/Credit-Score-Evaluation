import numpy as np
import normalization

user={

}

def MaturityIndex(age,years_in_business):
    cred=0
    #years in business has a weight of 60% here
    weight_years_in_business = 0.6
    cred+=normalization.normalize_business_duration(C6=years_in_business)*weight_years_in_business

    #age has a weight of 40%
    weight_age=0.4
    cred+=normalization.normalize_age(B3=age)*weight_age
    return cred

def CreditAccounts(num_credit_accounts,total_open_contracts):
    cred=0
    weight=0.5#both share the same weights
    for variable in [num_credit_accounts, total_open_contracts]:
        if variable < 0:
            continue  # Handle negative values (if applicable)
        if variable < 2:
            cred+= weight
        elif variable < 4:
            cred += 0.8 * weight
        elif variable < 6:
            cred += 0.6 * weight
        elif variable<8:
             cred+=0.4*weight
        else:cred+=0
    return cred

def is_dead(user):
    # Define weights for each factor
    weights = {
        'lack_financial_documentation': 0.15 if normalization.is_EMPTY(user.get("D6",0)) and normalization.is_EMPTY(user.get("E1","unknown")) else 0,
        'negative_credit_history': 0.25*CreditAccounts(num_credit_accounts=user.get("num_credit_accounts",0),
                                                       total_open_contracts=user.get("total_open_contracts",0)),
        'high_debt_to_income_ratio': 0.2*normalization.debt_to_income(total_amount_in_debt=user.get("total_amount_in_debt"),
                                                                       revenue=user.get("D8",0)),
        'business_instability': 0.15*normalization.normalize_revenue(D8=user.get("D8",0),
                                                                     D6=user.get("D6",0),
                                                                     D7=user.get("D7",0),
                                                                     D9=user.get("D9",0),
                                                                     D10=user.get("D10",0)),
        'lack_collateral': 0.1 if normalization.is_EMPTY==True else 0,
        'high_risk_location': 0.05*normalization.normalize_rgp(B5=user.get("B5",0)),
        'inadequate_management_experience': 0.1*MaturityIndex(age=user.get("age",0),years_in_business=user.get("C6",0)),
    }

    # Calculate weighted risk score
    risk_score = weights['high_risk_location']+\
                weights['inadequate_management_experience']+\
                weights['negative_credit_history']+\
                weights['lack_collateral']+\
                weights['high_debt_to_income_ratio']+\
                weights['business_instability']
    
    # Normalize risk score to ensure it's between 0 and 1
    norm= min(max(risk_score, 0), 1)
    if(norm<0.5):
        return True
    else:return False




