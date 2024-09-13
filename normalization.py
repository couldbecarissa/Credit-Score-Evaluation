import numpy as np
import pandas as pd

def normalize_business_duration(C6):
    weights = [0.2, 0.4,0.6, 0.8, 1.0]
    business_duration_ranges = [(0, 3), (3, 5), (5, 8), (8,11),(11, 1000)]
    for start, end in business_duration_ranges:
        if start <= C6 < end:
            weight= weights[business_duration_ranges.index((start, end))]     
        else: weight=0
    return weight  

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
    # Read the CSV file
    df = pd.read_csv('regionaldata.csv')
    # Convert region names to lowercase and strip whitespace for case-insensitive matching
    df['Region_Lower'] = df['Region'].str.lower().str.strip()
    region_name_lower = B5.lower().strip()
    
    # Find the matching row
    matching_row = df[df['Region_Lower'] == region_name_lower]
    
    if not matching_row.empty:
        # If a match is found, return the Normalized_GDP value
        gdp = matching_row['Normalized_GDP'].iloc[0]
    else:
        # If no match is found, return None
        gdp=0
    return gdp

def normalize_market(market):
    df = pd.read_csv('regionaldata.csv')
    def min_max_norm(data):
        min=np.min(data)
        max=np.max(data)
        scaled_data=(data- min) / (max - min)
        return scaled_data
    
    df['Norm_Mean']=min_max_norm(df['Mean'])    

    df['Market_Lower']=df['Market'].str.lower().str.strip()
    market=market.lower()
    matching_row= df[df['Market_Lower'] == market]
    if not matching_row.empty:
            # If a match is found, return the Normalized_GDP value
            market_mean = matching_row['Norm_Mean'].iloc[0]
    else:
            # If no match is found, return None
            market_mean=0
    return market_mean

def is_EMPTY(field):
    if field is not None:
        return True
    else:return False

def debt_to_income(total_amount_in_debt,revenue):
    total_amount_in_debt=total_amount_in_debt/12
    d2i=min(max(total_amount_in_debt/revenue, 0), 1) if revenue!=0 else 0
    return d2i

def normalize_overdue_installments(num_overdue_installments):
    overdue_ranges = [(0, 3), (3, 5),(5,7),(7,9),(9,11),(11,13),(13,15),(15, float('inf'))]
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

def normalize_PPI_score(PPIscore):
    PPI_ranges=[(40,45),(45,50),(50,55),(55,60),(60,65),(65,70),(70,75),(75,80),(80,85),(85,90),(90,95),(95,100)]
    weights=[(1/12),(1/6),0.25,(1/3),(5/12),0.5,(7/12),(2/3),0.75,(5/6),11/12,1]
    for start,end in PPI_ranges:
        if start<=PPIscore<end:
            wt=weights[PPI_ranges.index((start,end))]
        else:wt=0
    return wt