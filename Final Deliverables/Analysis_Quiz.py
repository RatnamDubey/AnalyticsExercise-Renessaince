# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 19:24:22 2017

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

sub_16.rename(columns ={'School ID' : 'ID'} , inplace=True)
sub_17.rename(columns ={'School ID' : 'ID'} , inplace=True)
demographic.rename(columns ={'School ID' : 'ID'} , inplace=True)
quiz_act.rename(columns ={'School ID' : 'ID'} , inplace=True)


# Combining the Columns as to get more info on the Data 
#Combining the Data with Quiz Information 
sub_16_quiz = pd.merge(sub_16, quiz_act, on='ID')
sub_17_quiz = pd.merge(sub_17, quiz_act, on='ID')


#Exploring the Data 
sub_16_quiz.head(5)

sub_16_quiz.columns = [c.replace(' ', '_') for c in sub_16_quiz.columns]
sub_17_quiz.columns = [c.replace(' ', '_') for c in sub_17_quiz.columns]

#Finding the KPI (Key performance Indicators )
sub_16_quiz['Avg_Sell_price'] = sub_16_quiz['Expiring_Dollars']/sub_16_quiz['Expiring_Students']
sub_17_quiz['Avg_Sell_price'] = sub_17_quiz['Expiring_Dollars']/sub_17_quiz['Expiring_Students']

# Are we Experiencing any time lag ??
sub_16_quiz['Renewal_Date'] = sub_16_quiz['Renewal_Date'].apply(pd.to_datetime)
sub_16_quiz['Subscription_End_Date'] = sub_16_quiz['Subscription_End_Date'].apply(pd.to_datetime)

sub_16_quiz['Renew_delay'] = sub_16_quiz['Renewal_Date'] - sub_16_quiz['Subscription_End_Date']
sub_16_quiz['Renew_delay'] = sub_16_quiz['Renew_delay'] / np.timedelta64(1, 'D')


sub_17_quiz['Renewal_Date'] = sub_17_quiz['Renewal_Date'].apply(pd.to_datetime)
sub_17_quiz['Subscription_End_Date'] = sub_17_quiz['Subscription_End_Date'].apply(pd.to_datetime)

sub_17_quiz['Renew_delay'] = sub_17_quiz['Renewal_Date'] - sub_17_quiz['Subscription_End_Date']
sub_17_quiz['Renew_delay'] = sub_17_quiz['Renew_delay'] / np.timedelta64(1, 'D')

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
    
    
sub_16_quiz["Days_group"] = sub_16_quiz['Renew_delay'].map(transform_diff_grp)
sub_17_quiz["Days_group"] = sub_17_quiz['Renew_delay'].map(transform_diff_grp)

#Fillling non Renewal Data with 11 

sub_16_quiz['Days_group'].fillna(11, inplace=True)
sub_17_quiz['Days_group'].fillna(11, inplace=True)

# Filling the Null values with ZZ in place of NA 

sub_16_quiz.fillna('ZZ', inplace=True)
sub_17_quiz.fillna('ZZ', inplace=True)

# DiviDing the Data in renewed and Not Renewed Data 

sub_16_quiz_ren = sub_16_quiz[sub_16_quiz['Subscription_Status']== "Renewed"]
sub_16_quiz_nonren = sub_16_quiz[sub_16_quiz['Subscription_Status']== "Not Renewed"]

sub_17_quiz_ren = sub_17_quiz[sub_17_quiz['Subscription_Status']== "Renewed"]
sub_17_quiz_nonren = sub_17_quiz[sub_17_quiz['Subscription_Status']== "Not Renewed"]

#Checking the Pattern in the Renew Data 

 
# OverAll USA Students Grade 
sub_16_quiz_ren.groupby(['Grade'])['State'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_quiz_nonren.groupby(['Grade'])['State'].count().plot(kind="Bar" , title= "2016 NON Renew Data")
#Checking for 2017 Data 
sub_17_quiz_ren.groupby(['Grade'])['State'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_quiz_nonren.groupby(['Grade'])['State'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# NO Change in the Grade Pattern



# OverAll USA Students School Year 
sub_16_quiz_ren.groupby(['School_Year'])['State'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_quiz_nonren.groupby(['School_Year'])['State'].count().plot(kind="Bar" , title= "2016 NON Renew Data")
#Checking for 2017 Data 
sub_17_quiz_ren.groupby(['School_Year'])['State'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_quiz_nonren.groupby(['School_Year'])['State'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Difference in School year of 2016 and 2017 Data - Non Renewed 
# In 2016 Ron Renew Data the School year 2016-17 are less compare to 
#2017 Ron Renew Data 

# OverAll USA Active Student 
sub_16_quiz_ren.groupby(['State'])['Active_Students'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_quiz_nonren.groupby(['State'])['Active_Students'].count().plot(kind="Bar" , title= "2016 NON Renew Data")
#Checking for 2017 Data 
sub_17_quiz_ren.groupby(['State'])['Active_Students'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_quiz_nonren.groupby(['State'])['Active_Students'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Difference in TExas Student Renewed in 2016and 2017 Rest all are quite same 
# Non Active Students Difference in the State of Florida for 2016 and 2017 Data

# OverAll USA Active Student 
sub_16_quiz_ren.groupby(['State'])['Quizzes_Taken'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_quiz_nonren.groupby(['State'])['Quizzes_Taken'].count().plot(kind="Bar" , title= "2016 NON Renew Data")
#Checking for 2017 Data 
sub_17_quiz_ren.groupby(['State'])['Quizzes_Taken'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_quiz_nonren.groupby(['State'])['Quizzes_Taken'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Difference in TExas Student Renewed in 2016 and 2017 Rest all are quite same 

# OverAll USA Active Student 
sub_16_quiz_ren.groupby(['State'])['Quizzes_Passed'].count().plot(kind="Bar" , title= "2016 Renew Data")
sub_16_quiz_nonren.groupby(['State'])['Quizzes_Passed'].count().plot(kind="Bar" , title= "2016 NON Renew Data")
#Checking for 2017 Data 
sub_17_quiz_ren.groupby(['State'])['Quizzes_Passed'].count().plot(kind="Bar" , title= "2017 Renew Data")
sub_17_quiz_nonren.groupby(['State'])['Quizzes_Passed'].count().plot(kind="Bar" , title= "2017 NON Renew Data")

# Difference in TExas Student Renewed in 2016 and 2017 Rest all are quite same 

















