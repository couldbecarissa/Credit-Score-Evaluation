import numpy as np
import pandas as pd

def normalize_business_duration(C6):
    """
    Normalize business duration (C6) to a 0-1 scale.
    """
    weights = [0.2, 0.4,0.6, 0.8, 1.0]
    business_duration_ranges = [(0, 2), (3, 5), (6, 8), (9,11),(12, float('inf'))]
    for start, end in business_duration_ranges:
        if start <= C6 < end:
            return weights[business_duration_ranges.index((start, end))]     
        else: return 0  


def normalize_payment_methods(C7):
    """
    Normalize payment methods (C7) to a 0-1 scale.
    """
    if 'cash' in C7 :
        return 0.33
    elif 'cash' in C7 and 'mobile money' in C7 :
        return 0.67
    elif 'cash' in C7 and 'mobile money' in C7 and 'bank' in C7:
        return 1.00
    else:
        return 0.00  # Default case for unexpected combinations

def normalize_age(B3):
    """
    Normalize age category (B3) to a 0-1 scale.
    """
    age_scores = {
        '18-24': 0.25,
        '25-34': 0.50,
        '35-44': 0.75,
        '45+': 1.00
    }
    return age_scores.get(B3, 0.00)

def normalize_revenue(D6, D7, D8, D9, D10):
    """
    Normalize revenue (D6 to D10) to a 0-1 scale using percentiles.
    """
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
    scores = [1/6,1/3,1/2,2/3,5/6,1]
    
    for i, threshold in enumerate(percentiles[1:]):
        if monthly_revenue <= threshold:
            return scores[i]
    
    return 1.00  # Default to highest score if above all thresholds

def normalize_ppi_score(ppi_score):
    """
    Normalize PPI score to a 0-1 scale, inverting so lower poverty likelihood
    results in a higher credit score.
    """
    return (100 - ppi_score) / 100

def min_max_normalize(value, min_val, max_val):
    """
    Perform min-max normalization on a single value.
    """
    return (value - min_val) / (max_val - min_val)

def z_score_normalize(value, mean, std_dev):
    """
    Perform z-score normalization on a single value.
    """
    return (value - mean) / std_dev

def normalize_categorical(category, category_order):
    """
    Normalize a categorical variable based on a predefined order.
    """
    return category_order.index(category) / (len(category_order) - 1)

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
    if(monthly_demo_affordability<=0):
            cred+=0
    affordability_ratios=[1/8,1/4,3/8,1/2,5/8,3/4,7/8,1]
    for ratio in affordability_ratios:
        if(monthly_demo_affordability<=ratio*total_amount_in_debt):
            return ratio
        else: return 0

def normalize_rgp(B5):
    rgp=pd.read_csv('normalized-tanzania-gdp-csv.txt')
    for region in rgp['Region']:
        if(B5==region):
             index_find=rgp[rgp['Region'].astype(str).str.lower() == B5.str.lower()]
             index=index_find.index[0]
             return rgp.loc[index, 'Normalized GDP']
            
        else:return 0
 #POLITICAL INSTABILITY

def is_EMPTY(field):
    if field is not None:
        return True
    else:return False

def debt_to_income(total_amount_in_debt,revenue):
    total_amount_in_debt=total_amount_in_debt/12
    d2i=min(max(total_amount_in_debt/revenue, 0), 1) if revenue!=0 else 0
    return d2i