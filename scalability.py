import pandas as pd
import numpy as np


def ScaledPaymentHistory(max_past_due_days,max_past_due_amount,total_amount_in_debt,num_overdue_installments,monthly_demo_affordability):
    cred=1
    #Weight for the maximum days past the due date for payment is 25%
    weight_past_due_days = 0.25
    past_due_ranges = [(0, 5),(6,10),(11,20),(21,30),(31,40),(41,50),(51,60),(61,float('inf'))]
    weights = [1, 7/8,3/4,5/8,0.5,3/8,0.25,1/8,0]

    for start, end in past_due_ranges:
        if start <= max_past_due_days < end:
            cred -= weights[past_due_ranges.index((start, end))] * weight_past_due_days
            break
    
    #Weight 0f the maximum unpaid due amount is 30%
    weight_past_due_amount=0.3
    if(max_past_due_amount==0 or max_past_due_amount<monthly_demo_affordability):
        cred-=weight_past_due_amount
    elif(max_past_due_amount>monthly_demo_affordability):
        cred-=0.4*weight_past_due_amount
    else:cred-=0

    weight_total_amount_in_debt=0.2
    debt_ranges = [(0, 50000), (50000, 100000), (100000, 150000),(150000,200000),(200000,250000),(250000,300000),(300000,350000),(350000,400000),(400000,450000),(450000,500000)]
    weights_debt_amount = [1, 0.9, 0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]

    for start, end in debt_ranges:
        if start <= total_amount_in_debt < end:
            cred -= weights_debt_amount[debt_ranges.index((start, end))] * weight_total_amount_in_debt
            return cred
        
    weight_num_overdue_installments=0.25
    overdue_ranges = [(0, 2), (3, 5), (5, float('inf'))]
    weights = [1, 0.6, 0.3]

    for start, end in overdue_ranges:
        if start <= num_overdue_installments < end:
            cred -= weights[overdue_ranges.index((start, end))] * weight_num_overdue_installments
            break

    return cred
    

    