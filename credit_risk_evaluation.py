#Load the librarys
import pandas as pd 
import numpy as np 
import scalability
from scalability import ScaledPaymentHistory
import normalization

#Overall Function Weights
weight_CreditUtilization=0.2
weight_PaymentHistory=0.5
weight_MaturityIndex=0.05
weight_LoanTerm=0.1
weight_CreditAccounts=0.15

#Finding a credit utilization score
def CreditUtilization(financial_literacy,total_amount_in_debt,customer_payment_method,housing_situation,own_vs_rent,emergency_handling):
    cred=0
    #weight for financial literacy=20%,remaining=80%
    if(financial_literacy=="yes"):
        cred+=0.2
    elif financial_literacy=="no":
         cred+=0
        #weight for total amount in debt=30%,remaining=50%
    weight_amount_in_debt = 0.3
    cred+=normalization.normalize_debt(debt=total_amount_in_debt)*weight_amount_in_debt
    #weight for customer payment method=25%,remaining=25%
    weight_payment=0.25
    cred+=normalization.normalize_payment_methods(C7=customer_payment_method)*weight_payment

    #last 25%for housing issues and situations
    weight_housing=0.75*0.3#It takes up 75% of the 25%
    cred+=normalization.normalize_dependants(dependants=housing_situation)*weight_housing
        
    weight_ownership=0.25*0.25  #Takes up 25% of the 25%
    if(own_vs_rent=="own"):
        cred+=weight_ownership
    elif(own_vs_rent=="rent"):
            cred+=0.3*weight_ownership
    else:cred+=0

    return cred

def MaturityIndex(age,years_in_business):
    cred=0
    #years in business has a weight of 60% here
    weight_years_in_business = 0.6
    cred+=normalization.normalize_business_duration(C6=years_in_business)*weight_years_in_business

    #age has a weight of 40%
    weight_age=0.4
    cred+=normalization.normalize_age(B3=age)*weight_age
    return cred

def PaymentHistory(total_amount_in_debt,monthly_demo_affordability,num_overdue_installments,num_credit_inquiries,max_past_due_amount,max_past_due_days,loan_term,household_region):
    cred=0
    #Starting with 20% for monthly demonstrated affordability
    weight_monthly_affordability=0.2
    cred+=normalization.normalize_affordability(monthly_demo_affordability=monthly_demo_affordability,
                                                total_amount_in_debt=total_amount_in_debt)*weight_monthly_affordability
    

    #Number of overdue installments has a 25% weight here
    weight_overdue_installments = 0.25
    overdue_ranges = [(0, 2), (3, 5), (5, float('inf'))]
    weights = [1, 0.6, 0.3]

    for start, end in overdue_ranges:
        if start <= num_overdue_installments < end:
            cred += weights[overdue_ranges.index((start, end))] * weight_overdue_installments
            break

    #Number of credit enquiries is at 15% weight here
    weight_credit_inquiries=0.15
    credit_inquiry_ranges = [(0, 1), (1, 4), (4, 6)]
    weights = [1, 1/3, 2/3]

    for start, end in credit_inquiry_ranges:
        if start <= num_credit_inquiries < end:
            cred += weights[credit_inquiry_ranges.index((start, end))] * weight_credit_inquiries
            break

    #Highest past due amount has a 10% weight here
    weight_past_due_amount=0.1
    if(max_past_due_amount==0 or max_past_due_amount<monthly_demo_affordability):
        cred+=weight_past_due_amount
    elif(max_past_due_amount>monthly_demo_affordability):
        cred+=0.4*weight_past_due_amount
    else:cred+=0

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
    cred+=normalization.normalize_rgp(B5=household_region)*weight_rgp

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

def LoanTerm(loan_term,loan_interest_rate):
    cred=0
    #here the period for payment has the weight of 70%
    weight_payback_period=0.7
    if(loan_term=="one week"):
        cred+=0.5*weight_payback_period
    elif(loan_term=="two weeks"):
        cred+=0.7*weight_payback_period
    elif(loan_term=="a month"):
        cred+=weight_payback_period
        return cred

    #interest rate has a weight of 30%
    weight_loan_interest = 0.3
    interest_rate_ranges = [(0, 5), (5, 10), (10, 15), (15, 20)]
    weights = [1, 0.5, 0.2, 0.1]

    for start, end in interest_rate_ranges:
        if start <= loan_interest_rate < end:
            cred += weights[interest_rate_ranges.index((start, end))] * weight_loan_interest
        break
    return cred

"""
Results from the above functions are in the range (0,1)
"""
def calculate_credit_score(financial_literacy,
                           total_amount_in_debt,
                           customer_payment_method,
                           housing_situation,
                           own_vs_rent,
                           emergency_handling,
                           age,years_in_business,
                           monthly_demo_affordability,
                           num_overdue_installments,num_credit_inquiries,
                           max_past_due_amount,max_past_due_days,
                           loan_term,
                           num_credit_accounts,total_open_contracts,loan_interest_rate,household_region  
):
            credit_util=CreditUtilization(financial_literacy=financial_literacy,
                                          total_amount_in_debt=total_amount_in_debt,
                                          customer_payment_method=customer_payment_method,
                                          housing_situation=housing_situation,
                                          own_vs_rent=own_vs_rent,
                                          emergency_handling=emergency_handling)
            maturity_index=MaturityIndex(age=age,years_in_business=years_in_business)
            payment_history=PaymentHistory(monthly_demo_affordability=monthly_demo_affordability,
                                           num_credit_inquiries=num_credit_inquiries,
                                           num_overdue_installments=num_overdue_installments,
                                           max_past_due_amount=max_past_due_amount,
                                           max_past_due_days=max_past_due_days,
                                           loan_term=loan_term,
                                           household_region=household_region,
                                           total_amount_in_debt=total_amount_in_debt)
            credit_accounts=CreditAccounts(num_credit_accounts=num_credit_accounts,
                                           total_open_contracts=total_open_contracts)
            loan_terms=LoanTerm(loan_term=loan_term,loan_interest_rate=loan_interest_rate)

            credit_score=(weight_CreditAccounts*credit_accounts)+\
            (weight_CreditUtilization*credit_util)+(weight_LoanTerm*loan_terms)+\
                (weight_MaturityIndex*maturity_index)+(weight_PaymentHistory*payment_history)
            return credit_score


def approve_loan(credit_score):
    max_loan_amount=500000
    min_loan_amount=50000
    min_credit_score=(min_loan_amount/max_loan_amount)-0.01
    if(credit_score<min_credit_score):
        print("Sorry,you do not qualify for a loan.")
    else: loan=credit_score*max_loan_amount
    return loan


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

credit_score_user=calculate_credit_score(
            financial_literacy = user.get("financial_literacy", "unknown"),
            total_amount_in_debt = user.get("total_amount_in_debt", 0),
            customer_payment_method = user.get("customer_payment_method", "unknown"),
            housing_situation = user.get("housing_situation", 0),
            own_vs_rent = user.get("own_vs_rent", "unknown"),
            emergency_handling = user.get("emergency_handling", "unknown"),
            age = user.get("age", 0),
            years_in_business = user.get("years_in_business", 0),
            monthly_demo_affordability = user.get("monthly_demo_affordability", 0),
            num_overdue_installments = user.get("num_overdue_installments", 0),
            num_credit_inquiries = user.get("num_credit_inquiries", 0),
            max_past_due_amount = user.get("max_past_due_amount", 0),
            max_past_due_days = user.get("max_past_due_days", 0),
            loan_term = user.get("loan_term", "unknown"),
            num_credit_accounts = user.get("num_credit_accounts", 0),
            total_open_contracts = user.get("total_open_contracts", 0),
            loan_interest_rate=user.get("loan_interest_rate",0),
            household_region=user.get("household_region",0)
            )
#I will write another function to determine whether of not the credit score should be scaled
scaled_credit_score_user=credit_score_user-(1-ScaledPaymentHistory(max_past_due_days=user.get("max_past_due_days", 0),
                                      max_past_due_amount=user.get("max_past_due_amount", 0),
                                      total_amount_in_debt=user.get("total_amount_in_debt", 0),
                                      num_overdue_installments= user.get("num_credit_inquiries", 0),
                                      monthly_demo_affordability=user.get("monthly_demo_affordability", 0)
                                      ))

print(f"User Credit Score: {credit_score_user:,} creds")
print(f"User Scaled Credit Score: {scaled_credit_score_user:,} creds")

loan_given=approve_loan(credit_score=credit_score_user)
print(loan_given)