#Load the librarys
import pandas as pd 
import numpy as np 
import normalization
import dead_cases

#Overall Function Weights
weight_CreditUtilization=0.2
weight_PaymentHistory=0.5
weight_MaturityIndex=0.05
weight_LoanTerm=0.1
weight_CreditAccounts=0.15

#Finding a credit utilization score
def CreditUtilization(financial_literacy,total_amount_in_debt,C7,B15,C3):
    cred=0
    #weight for financial literacy=10%,remaining=90%
    if(financial_literacy=="yes"):
        cred+=0.1
    elif financial_literacy=="no":
         cred+=0
        #weight for total amount in debt=60%,remaining=30%
    weight_amount_in_debt = 0.6
    cred+=normalization.normalize_debt(debt=total_amount_in_debt)*weight_amount_in_debt

    #weight for customer payment method=15%,remaining=15%
    weight_payment=0.15
    cred+=normalization.normalize_payment_methods(C7=C7)*weight_payment

    #last 25%for housing issues and situations
    weight_housing=0.75*0.15#It takes up 75% of the 15%
    cred+=normalization.normalize_dependants(dependants=B15)*weight_housing
        
    weight_ownership=0.25*0.15  #Takes up 25% of the 15%
    if(C3=="own"):
        cred+=weight_ownership
    elif(C3=="rent"):
            cred+=0.3*weight_ownership
    else:cred+=0

    return cred

def MaturityIndex(age,C6):
    cred=0
    #years in business has a weight of 60% here
    weight_years_in_business = 0.6
    cred+=weight_years_in_business*normalization.normalize_business_duration(C6=C6)

    #age has a weight of 40%
    weight_age=0.4
    cred+=weight_age*normalization.normalize_age(B3=age)

    return cred

def PaymentHistory(total_amount_in_debt,monthly_demo_affordability,num_overdue_installments,num_credit_inquiries,max_past_due_amount,max_past_due_days,B5):
    cred=0
    #Starting with 20% for monthly demonstrated affordability
    weight_monthly_affordability=0.2
    cred+=normalization.normalize_affordability(monthly_demo_affordability=monthly_demo_affordability,
                                                total_amount_in_debt=total_amount_in_debt)*weight_monthly_affordability
    

    #Number of overdue installments has a 25% weight here
    weight_overdue_installments = 0.25
    cred+=weight_overdue_installments*normalization.normalize_overdue_installments(num_overdue_installments=num_overdue_installments)

    #Number of credit enquiries is at 15% weight here
    weight_credit_inquiries=0.15
    cred+=weight_credit_inquiries*normalization.normalize_credit_inquiries(num_credit_inquiries=num_credit_inquiries)

    #Highest past due amount has a 10% weight here
    weight_past_due_amount=0.1
    if(max_past_due_amount==0 or max_past_due_amount<monthly_demo_affordability):
        cred+=weight_past_due_amount
    elif(max_past_due_amount>monthly_demo_affordability):
        cred+=0.4*weight_past_due_amount

    #Highest Past Due days has a 10% weight here
    weight_past_due_days = 0.1
    past_due_ranges = [(0, 20),(20,40),(40,60),(60,80),(80,100),(100,120),(120,140),(140,160),(160,180),(180,float('inf'))]
    weights = [1, 0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0]

    for start, end in past_due_ranges:
        if start <= max_past_due_days < end:
            cred += weights[past_due_ranges.index((start, end))] * weight_past_due_days
            break
    
    #Regional GDP has a weight of 20%
    weight_rgp=0.2
    cred+=normalization.normalize_rgp(B5=B5)*weight_rgp

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

def LoanTerm(loan_term):
    cred=0
    #here the period for payment has the weight of 100%
    weight_payback_period=1
    if(loan_term==7):
        cred+=0.5*weight_payback_period
    elif(loan_term==15):
        cred+=0.7*weight_payback_period
    elif(loan_term==30):
        cred+=weight_payback_period
    
    return cred


"""
Results from the above functions are in the range (0,1)
"""
def calculate_credit_score(user):
            credit_util=CreditUtilization(financial_literacy=user.get("financial_literacy","unknown"),
                                          total_amount_in_debt=user.get("total_amount_in_debt",0),
                                          C7=user.get("C7", "unknown"),
                                          B15=user.get("B15", 0),
                                          C3=user.get("C3", 0))
            maturity_index=MaturityIndex(age=user.get("age", 0),
                                         C6=user.get("C6", 0),)
            payment_history=PaymentHistory(
                                            total_amount_in_debt=user.get("total_amount_in_debt", 0),
                                            monthly_demo_affordability=user.get("monthly_demo_affordability", 0),
                                            num_overdue_installments=user.get("num_overdue_installments", 0),
                                           num_credit_inquiries=user.get("num_credit_inquiries", 0),
                                           max_past_due_amount=user.get("max_past_due_amount", 0),
                                           max_past_due_days=user.get("max_past_due_days", 0),
                                           B5=user.get("B5", "Dar")
                                           )
            credit_accounts=CreditAccounts(num_credit_accounts=user.get("num_credit_accounts", 0),
                                           total_open_contracts=user.get("total_open_contracts", 0))
            loan_terms=LoanTerm(loan_term=user.get("loan_term",7))
            credit_score=(weight_CreditAccounts*credit_accounts)+\
            (weight_CreditUtilization*credit_util)+(weight_LoanTerm*loan_terms)+\
                (weight_MaturityIndex*maturity_index)+(weight_PaymentHistory*payment_history)
            return credit_score

def approve_loan(credit_score):
    max_loan_amount=500000
    min_loan_amount=50000
    min_credit_score=0.3
    if credit_score>min_credit_score:
        if credit_score <= 0.5:
            scaled_score = credit_score**2
        else:
            scaled_score = 0.5 + 0.5 * ((credit_score - 0.5) / 0.5) 

        loan = min_loan_amount + (max_loan_amount - min_loan_amount) * scaled_score
    else:loan=0
    return loan

def should_calculate(user):
    calculate=dead_cases.is_dead(user=user)
    if calculate==True:
        credit_score_user=calculate_credit_score(user=user)
        return credit_score_user
    else: raise ValueError("You are not eligible for a loan")