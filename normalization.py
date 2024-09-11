import numpy as np
import pandas as pd

def normalize_business_duration(C6):
    weights = [0.2, 0.4,0.6, 0.8, 1.0]
    business_duration_ranges = [(0, 2), (3, 5), (6, 8), (9,11),(12, float('inf'))]
    for start, end in business_duration_ranges:
        if start <= C6 < end:
            return weights[business_duration_ranges.index((start, end))]     
        else: return 0  

def normalize_payment_methods(C7):
    if 'cash' in C7 :
        return 0.33
    elif 'cash' in C7 and 'mobile money' in C7 :
        return 0.67
    elif 'mobile money' in C7 or 'cash' in C7 and 'bank' in C7:
        return 0.5
    elif 'bank' in C7:
        return 0.7
    elif 'mobile money' in C7 and 'bank' in C7:
        return 0.9
    elif 'cash' in C7 and 'mobile money' in C7 and 'bank' in C7:
        return 1.00
    else:
        return 0.00  

def normalize_age(B3):
    age_scores = {
        (18,24): 0.25,
        (25,34): 0.50,
        (35,44): 0.75,
        (45,np.float64('inf')): 1.00}
    
    for (lower, upper), score in age_scores.items():
        if lower <= B3 <= upper:
            return score
    return score

def normalize_revenue(D6, D7, D8, D9, D10):
    # Convert all revenues to monthly
    monthly_revenue = max(
        D6 * 30,
        D7 * 4,
        D8,
        D9 / 3,
        D10 / 12
    )
    
    # Define percentile thresholds (these should be calculated from your dataset)
    percentiles = [0, 50000, 100000,200000, 500000, 700000, float('inf')]
    scores = [(1/8),0.25,(3/8),0.5,(5/8),0.75,(7/8),1]
    
    for i, threshold in enumerate(percentiles[1:]):
        if monthly_revenue <= threshold:
             wt=scores[i]
        else:wt=0
    
    return wt # Default to highest score if above all thresholds

def normalize_dependants(dependants):
    dependant_ranges=[(0,2),(2,4),(4,6),(6,8),(8,10),(10,np.float64('inf'))]
    weights_housing_amount=[1,5/6,2/3,1/2,1/3,1/6]
    for start,end in dependant_ranges:
        if start<=dependants<end:
            return weights_housing_amount[dependant_ranges.index((start,end))]
        else:return 0

def normalize_debt(debt):
    debt_ranges = [(0, 50000), (50000, 100000), (100000, 150000),(150000,200000),(200000,250000),(250000,300000),(300000,350000),(350000,400000),(400000,450000),(450000,500000)]
    weights_debt_amount = [1, 0.9, 0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]

    for start, end in debt_ranges:
        if start <= debt < end:
            return weights_debt_amount[debt_ranges.index((start, end))]
        else: return 0

def normalize_affordability(monthly_demo_affordability,total_amount_in_debt):
    if total_amount_in_debt!=0:
        ratio=monthly_demo_affordability/total_amount_in_debt
        if ratio>1:
            ratio=1
        elif ratio<0:
            ratio=0
    else:ratio=0
    return ratio

def normalize_rgp(B5):
    rgp=pd.read_csv('normalized-tanzania-gdp-csv.txt')
    for region in rgp['Region']:
        if(B5==region):
             index=rgp[rgp['Region'].astype(str).lower() == B5.str.lower()].index[0]
             result=rgp.at[index, 'Normalized GDP']
        else:result=0
    return result
 #POLITICAL INSTABILITY

def is_EMPTY(field):
    if field is not None:
        return True
    else:return False

def debt_to_income(total_amount_in_debt,revenue):
    total_amount_in_debt=total_amount_in_debt/12
    d2i=min(max(total_amount_in_debt/revenue, 0), 1) if revenue!=0 else 0
    return d2i

def normalize_overdue_installments(num_overdue_installments):
    overdue_ranges = [(0, 2), (3, 5),(5,7),(7,9),(9,11),(11,13),(13,15),(15, float('inf'))]
    weights = [1,(7/8),0.75,(5/8),0.5,(3/8),0.25,(1/8)]

    for start, end in overdue_ranges:
        if start <= num_overdue_installments < end:
            wt = weights[overdue_ranges.index((start, end))]
        else:wt=0
    return wt

def normalize_credit_inquiries(num_credit_inquiries):
    credit_inquiry_ranges = [(0, 1), (1, 3), (3, 6),(6,9),(9,12),(12,15),(15,np.float64('inf'))]
    weights = [1,(6/7),(5/7),(4/7),(3/7),(2/7),(1/7),0]

    for start, end in credit_inquiry_ranges:
        if start <= num_credit_inquiries < end:
            weight= weights[credit_inquiry_ranges.index((start, end))]
            break
    return weight