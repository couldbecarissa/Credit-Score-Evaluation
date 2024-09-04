#Load the librarys
import pandas as pd #To work with dataset
import numpy as np #Math library
import seaborn as sns #Graph library that use matplot in background
import matplotlib.pyplot as plt #to plot some parameters in seaborn

#Importing the data
df_credit = pd.read_csv('data2.csv',index_col=0)
#Searching for Missings,type of data and also known the shape of data
print(df_credit.info())
#Looking unique values
print(df_credit.nunique())
print(df_credit.describe())

#Finding a credit utilization score
def CreditUtilization(data):
    cred=0
    #weight for financial literacy=20%,remaining=80%
    if(data['financial_literacy']=="yes"):
        cred+=0.2
        return cred
        #weight for total amount in debt=30%,remaining=50%
    for amount in data['total_amount_in_debt']:
        start=50000
        steps=50000
        iter=8
        n=0
        while n<iter:
            if(amount>start and amount<=start+steps):
                cred+=0.075
                n+=1
                start+=steps
                return cred
    #weight for customer payment method=25%,remaining=25%
    for payment in data['customer_payment_method']:
        weight_payment=0.25
        if(payment=="cash"):
            cred+=0.5*weight_payment
        elif(payment=="mobile money" or payment=="bank payment"):
            cred+=0.2*weight_payment
        elif(payment=="loan"):
            cred+=0.1*weight_payment
        else:cred+=0
        return cred
    #last 25%for housing issues and situations
    for dependants in data['housing_situation']:
        weight_housing=0.25*0.3#It takes up 30% of the 25%
        if(dependants==0):
            cred+=0
        cred+=dependants/10*weight_housing
        return cred
    for ownership in data['own_vs_rent']:
        weight_ownership=0.25*0.25  #Takes up 25% of the 25%
        if(ownership=="own"):
            cred+=0.7*weight_ownership
        elif(ownership=="rent"):
            cred+=0.3*weight_ownership
        return cred  
    for emergency in data['emergency_handling']:#takes 45% of the 25%
        weight_emergency=0.45*0.25
        if(emergency=="dip into savings"):
            cred+=0.7*weight_emergency
        elif(emergency=="loan more"):
            cred=+0.3*weight_emergency
        else:cred+=0
        return cred
    return cred

df_credit2=df_credit.apply(CreditUtilization)
print(df_credit2)