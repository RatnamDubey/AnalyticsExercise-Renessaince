# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 19:44:32 2017

@author: dubey
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
le = preprocessing.LabelEncoder()


#Importing the Data 
demographic =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\demographic.csv" )
quiz_act =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\quiz_act.csv")
sub_16 =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\sub_data_15_16.csv")
sub_17 =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\sub_data_17.csv")

##Stripping the columns Name as they are npot consistant 

sub_16.columns = sub_16.columns.str.strip()
sub_17.columns = sub_17.columns.str.strip()
demographic.columns = demographic.columns.str.strip()
quiz_act.columns = quiz_act.columns.str.strip()

# Combining the Columns as to get more info on the Data 
#Combining the Data with demographic Information 

sub_16_demo = pd.merge(sub_16, demographic, on='Schooll_ID')
sub_17_demo = pd.merge(sub_17, demographic, on='Schooll_ID')

#Exploring the Data 
sub_16_demo.head(5)

sub_16_demo.columns = [c.replace(' ', '_') for c in sub_16_demo.columns]
sub_17_demo.columns = [c.replace(' ', '_') for c in sub_17_demo.columns]


#Grasping the demographic changes 
sub_16_demo.groupby(['Subscription_Status' ,'Metro_Code'])['Expiring_Dollars'].sum().plot(kind="Bar", title="2016 Demograpic Data")
sub_17_demo.groupby(['Subscription_Status' ,'Metro_Code'])['Expiring_Dollars'].sum().plot(kind="Bar" , title="2017 Demograpic Data")

#Cheking the Demographic Information Based on Avg Income 
demographic_op_1 = sub_16_demo.groupby(['Subscription_Status','Metro_Code' ,'Avg_Household_Income' ])['Expiring_Dollars'].sum()
demographic_op_1.to_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\Findings\\Demographic_op1.csv", index=True , header=True)

demographic_op_2 = sub_17_demo.groupby(['Subscription_Status','Metro_Code' ,'Avg_Household_Income' ])['Expiring_Dollars'].sum()
demographic_op_2.to_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\Findings\\Demographic_op2.csv", index=True , header=True)

#Checking the Demographic Information on Poverty Level

demographic_op_3 = sub_16_demo.groupby(['Subscription_Status','Metro_Code' ,'Poverty_Level_Code' ])['Expiring_Dollars'].count()
demographic_op_3.to_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\Findings\\Demographic_op3.csv", index=True , header=True)

demographic_op_4 = sub_17_demo.groupby(['Subscription_Status','Metro_Code' ,'Poverty_Level_Code' ])['Expiring_Dollars'].count()
demographic_op_4.to_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\Findings\\Demographic_op4.csv", index=True , header=True)

#Finding the KPI (Key performance Indicators )
sub_16_demo['Avg_Sell_price'] = sub_16_demo['Expiring_Dollars']/sub_16_demo['Expiring_Students']
sub_17_demo['Avg_Sell_price'] = sub_17_demo['Expiring_Dollars']/sub_17_demo['Expiring_Students']

# Checking the Impact of Average selling price on the Sales

sub_16_demo.groupby(['Avg_Sell_price' ,'Subscription_Status' ,'Metro_Code'])['Expiring_Dollars'].sum().plot(kind="Bar", title="2016 Demograpic Data")
sub_17_demo.groupby(['Avg_Sell_price' ,'Subscription_Status' ,'Metro_Code'])['Expiring_Dollars'].sum().plot(kind="Bar", title="2017 Demograpic Data")

# Are we Experiencing any time lag ??
sub_16_demo['Renewal_Date'] = sub_16_demo['Renewal_Date'].apply(pd.to_datetime)
sub_16_demo['Subs__End_Date'] = sub_16_demo['Subs__End_Date'].apply(pd.to_datetime)

sub_16_demo['Renew_delay'] = sub_16_demo['Renewal_Date'] - sub_16_demo['Subs__End_Date']
sub_16_demo['Renew_delay'] = sub_16_demo['Renew_delay'] / np.timedelta64(1, 'D')


sub_17_demo['Renewal_Date'] = sub_17_demo['Renewal_Date'].apply(pd.to_datetime)
sub_17_demo['Subs__End_Date'] = sub_17_demo['Subs__End_Date'].apply(pd.to_datetime)

sub_17_demo['Renew_delay'] = sub_17_demo['Renewal_Date'] - sub_17_demo['Subs__End_Date']
sub_17_demo['Renew_delay'] = sub_17_demo['Renew_delay'] / np.timedelta64(1, 'D')

#Grouping the Time Lag 
def transform_diff_grp(dl):
    if dl > 180 : return 10
    elif 150 < dl <= 180 : return 9
    elif 120 < dl <= 150 : return 8
    elif 90 < dl <= 120 : return 7
    elif 30 < dl <= 90 : return 6
    elif 0 <= dl <= 30 : return 5
    elif -30 < dl <= -1 : return 4
    elif -90 < dl <= -30 : return 3
    elif -150 <= dl <= -90 : return 2
    elif -400 < dl <= -151 : return 1
    
    
sub_16_demo["Days_group"] = sub_16_demo['Renew_delay'].map(transform_diff_grp)
sub_17_demo["Days_group"] = sub_17_demo['Renew_delay'].map(transform_diff_grp)

#Fillling non Renewal Data with 11 

sub_16_demo['Days_group'].fillna(11, inplace=True)
sub_17_demo['Days_group'].fillna(11, inplace=True)

sub_16_demo.groupby(['State'])['Days_group'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_17_demo.groupby(['State'])['Days_group'].count().plot(kind="Bar" , title="2017 Renew Data")

sub_16_demo_ren = sub_16_demo[sub_16_demo['Subscription_Status']== "Renewed"]
sub_16_demo_nonren = sub_16_demo[sub_16_demo['Subscription_Status']== "Not Renewed"]

sub_17_demo_ren = sub_17_demo[sub_17_demo['Subscription_Status']== "Renewed"]
sub_17_demo_nonren = sub_17_demo[sub_17_demo['Subscription_Status']== "Not Renewed"]

#Checking the Pattern in the Renew Data 

sub_16_demo_ren.groupby(['State'])['Days_group'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_17_demo_ren.groupby(['State'])['Days_group'].count().plot(kind="Bar" , title= "2017 Renew Data")

# Renew Data  Shows that there is sudden drop un the renew Data in the Texas State there is the Drop in 
# Texas State 

# 2016 

# Drop in the Renew pattern Previouslyin 2016 people book in 0 to 30 days after the renew gets over 
# Others Renew the subscription before 30 to 90 days back 
#People STart renewing in 2017 in before 30 to 90 days back 

#2017 

# Drop in the Renew pattern Previouslyin 2017 people book in 30 days  to 90 days before  the renew gets over 
# Others Renew the subscription in 0 to 30 days after the subscription got over 
#Reduction in 30 to 90 days afetr the subsciption 

# Non Renewed Subscription count both the years 

sub_16_demo_nonren.count()
sub_17_demo_nonren.count()

# Imputing the Missing Values 
sub_16_demo_ren.fillna('ZZ', inplace=True)
sub_17_demo_ren.fillna('ZZ', inplace=True)

sub_16_demo_nonren.fillna('ZZ', inplace=True)
sub_17_demo_nonren.fillna('ZZ', inplace=True)

# Checking with the Other Factors 
#Which Metro Code has maximumsubscriptions
#Checking for 2016 Data 


# K is unknown Metro Space 

sub_16_demo_ren.groupby(['Metro_Code'])['State'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Metro_Code'])['State'].count().plot(kind="Bar" , title= "2016 NON Renew Data")
#Checking for 2017 Data 

# K is unknown Metro Space 

sub_17_demo_ren.groupby(['Metro_Code'])['State'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Metro_Code'])['State'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Apple Mac Code Null value imputation 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Apple_Mac_Code'])['State'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Apple_Mac_Code'])['State'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Apple_Mac_Code'])['State'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Apple_Mac_Code'])['State'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Apple Mac Code "H" is high in Non renew Data of 2016 
# MIssing values are High in Both Renew and NOn renew Data 
# Renew Pattern is Same for 2016 and 2017 
# Non renew Pattern is Different from 2016 to 2017 

# PC Code Null value imputation 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['PC_Code'])['State'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['PC_Code'])['State'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['PC_Code'])['State'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['PC_Code'])['State'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# PC Code Missing values has been increased in 2017 compared to 2016 in renew Data 
# Non renew Data in 2016 and 2017 has same 

# Poverty Level Code Null value imputation 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Poverty_Level_Code'])['State'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Poverty_Level_Code'])['State'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Poverty_Level_Code'])['State'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Poverty_Level_Code'])['State'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# NO DIffererence in the Poverty Line 

# Average House hold Income Analyis 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Avg_Household_Income'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Avg_Household_Income'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Avg_Household_Income'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Avg_Household_Income'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Slight Decrease in the Avg House hold Income for the A Category A =  1-27,999
# Population is earning more Coz A is less in 2017 for Renew Data and Non Renew Data 
# But Avg is Still the Same 

# Title_1_Code  Analyis 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Title_1_Code'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Title_1_Code'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Title_1_Code'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Title_1_Code'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

#Identifies districts and public schools by the Title I per student district dollar allocation
# In 2017 both Renewed and Non Renewed Data "Category D " - D $500.00 Plus has been declined 
# Misssing Values has been Increased in 2017 

# Software_budget_per_head  Analyis 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Software_budget_per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Software_budget_per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Software_budget_per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Software_budget_per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Software budget G has decline for renew data 2017 
# Where as E $20 - $24  Category has been Increased  for Renewed Data and Non Reneweed Data 
# Slight Increasein Missing Values 

# Training_Budget_Per_head  Analyis 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Training_Budget_Per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Training_Budget_Per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Training_Budget_Per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Training_Budget_Per_head'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Traning budget E has decline for renew data 2017 E $11 - $13
# Where as D $9 - $10  Category has been Increased  for Non Reneweed Data 
#  Increasein Missing Values 

# Lunch_Program_Eligible_Students  Analyis 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Lunch_Program_Eligible_Students'])['Expiring_Dollars'].count().plot(kind="density" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Lunch_Program_Eligible_Students'])['Expiring_Dollars'].count().plot(kind="density" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Lunch_Program_Eligible_Students'])['Expiring_Dollars'].count().plot(kind="density" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Lunch_Program_Eligible_Students'])['Expiring_Dollars'].count().plot(kind="density" , title= "2017 NON Renew Data")

#  NO Changes 

# Affluence_Indicator  Analyis 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Affluence_Indicator'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Affluence_Indicator'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Affluence_Indicator'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Affluence_Indicator'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Slight increasse  in 3.0 and 4.0 in Non Renew Data in 2017 Compared to 2016 

sub_16_demo_ren.loc[(sub_16_demo_ren.Affluence_Indicator== 'ZZ') ,'Affluence_Indicator' ] = 6.0
sub_16_demo_nonren.loc[(sub_16_demo_nonren.Affluence_Indicator== 'ZZ') ,'Affluence_Indicator' ] = 6.0
sub_17_demo_ren.loc[(sub_17_demo_ren.Affluence_Indicator== 'ZZ') ,'Affluence_Indicator' ] = 6.0
sub_17_demo_nonren.loc[(sub_17_demo_nonren.Affluence_Indicator== 'ZZ') ,'Affluence_Indicator' ] = 6.0
                    
                    
# Avg_Sell_price  Analyis 
#Checking for 2016 Data 

sub_16_demo_ren.groupby(['Avg_Sell_price'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_demo_nonren.groupby(['Avg_Sell_price'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2016 NON Renew Data")

#Checking for 2017 Data 

sub_17_demo_ren.groupby(['Avg_Sell_price'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_demo_nonren.groupby(['Avg_Sell_price'])['Expiring_Dollars'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Average Selling Price Has been Increased Suddenly in the 2017 compared to 2018 
# For non Renewal Data the Scenario us Completely opposite as compared to 2016 
# 7.0 avg has been lower and the 8.0 has been higer 
# Concluding the Intution that the due to hike in the prices the sales are lower 


#Manupulating the Data for the Label Encoding 
# Creating the Training Data 
frames = [sub_16_demo_ren, sub_16_demo_nonren, sub_17_demo_ren]
Final_train = pd.concat(frames)

# Manupulating the Data , For Missing Data iMputing Random value 
# IN Subscription End Date and Renewal Date 

Final_train.loc[(Final_train.Subs__End_Date== 'ZZ') ,'Subs__End_Date' ] = 0
Final_train.loc[(Final_train.Renewal_Date== 'ZZ') ,'Renewal_Date' ] = 0
                
test = pd.DataFrame(sub_17_demo_nonren)
test['Subs__End_Date'] = test['Subs__End_Date'].apply(pd.to_datetime)

Final_train['Subs__End_Date'] = Final_train['Subs__End_Date'].apply(pd.to_datetime)
Final_train['Renewal_Date'] = Final_train['Renewal_Date'].apply(pd.to_datetime)

Final_train.loc[(Final_train.Renew_delay== 'ZZ') ,'Renew_delay' ] = 999
test.loc[(test.Renew_delay== 'ZZ') ,'Renew_delay' ] = 999

# Label Endoding with Train and TEst Data 
         
Final_train_Data = Final_train.apply(le.fit_transform)
test = test.apply(le.fit_transform)

# Checking the Corrrelation Matrix 
Corr_Analysis_Train = Final_train_Data.corr()
Corr_Analysis_Train.to_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\Findings\\Corr_Analysis_Train.csv", index=True , header=True)





