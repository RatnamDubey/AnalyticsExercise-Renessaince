# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 15:42:10 2017

@author: dubey
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Importing the Data 
demographic =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\demographic.csv" )
quiz_act =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\quiz_act.csv")
sub_16 =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\sub_data_15_16.csv")
sub_17 =  pd.read_csv("D:\\Analytics Excercise\\AnalyticsExercise\\Data\\sub_data_17.csv")

#Stripping Extra Space from the columns 
sub_16.rename(columns=lambda x: x.lstrip())
demographic.rename(columns=lambda x: x.strip())
sub_17.rename(columns=lambda x: x.strip())
quiz_act.rename(columns=lambda x: x.strip())

#Columns name 
sub_16.columns

sub_16.head(5)
sub_17.head(5)

#Converting the Dollar to numeric for analysis 
sub_16[' Expiring Dollars '] = sub_16[' Expiring Dollars '].str.replace(',', '')
sub_16[' Expiring Dollars '] = sub_16[' Expiring Dollars '].str.replace('$', '')
sub_16[' Expiring Dollars '] =  sub_16[' Expiring Dollars '].apply(pd.to_numeric)

sub_17[' Expiring Dollars '] = sub_17[' Expiring Dollars '].str.replace(',', '')
sub_17[' Expiring Dollars '] = sub_17[' Expiring Dollars '].str.replace('$', '')
sub_17[' Expiring Dollars '] =  sub_17[' Expiring Dollars '].apply(pd.to_numeric)

sub_16[' Expiring Students ']  = sub_16[' Expiring Students '].str.replace(',', '')
sub_16[' Expiring Students '] =  sub_16[' Expiring Students '].apply(pd.to_numeric)

#Checking the Subscription status for analysis 
sub_16_ren = sub_16[sub_16['Subscription Status'] == 'Renewed']
sub_16_nonren = sub_16[sub_16['Subscription Status'] == 'Not Renewed']
sub_17_ren = sub_17[sub_17['Subscription Status'] == 'Renewed']
sub_17_nonren = sub_17[sub_17['Subscription Status'] == 'Not Renewed']

#Merging all the three tables 
Sub_16_nonren_full = pd.merge(sub_16_nonren, demographic, on='School ID')
Sub_16_nonren_full = pd.merge(Sub_16_nonren_full, quiz_act, on='School ID')

Sub_17_nonren_full = pd.merge(sub_17_nonren, demographic, on='School ID')
Sub_17_nonren_full = pd.merge(Sub_17_nonren_full, quiz_act,  on='School ID')

Sub_16_ren_full = pd.merge(sub_16_ren, demographic, on='School ID')
Sub_16_ren_full = pd.merge(Sub_16_ren_full, quiz_act, on='School ID')

Sub_17_ren_full = pd.merge(sub_17_ren, demographic, on='School ID')
Sub_17_ren_full = pd.merge(Sub_17_ren_full, quiz_act,  on='School ID')



#Pltting the Demographic Data 
#Non Renewal Data 
Sub_16_nonren_full['Metro Code'].value_counts().plot(kind="pie" , autopct='%1.1f%%', startangle=270, fontsize=17 , title = '2016 NON Renewed Data')
plt.show()

Sub_17_nonren_full['Metro Code'].value_counts().plot(kind="pie" , autopct='%1.1f%%', startangle=270, fontsize=17 , title = '2017 NON Renewed Data')
plt.show()

# Renewal Data 
Sub_16_ren_full['Metro Code'].value_counts().plot(kind="pie" , autopct='%1.1f%%', startangle=270, fontsize=17  ,  title = '2016 Renewed Data')
plt.show()

Sub_17_ren_full['Metro Code'].value_counts().plot(kind="pie" , autopct='%1.1f%%', startangle=270, fontsize=17  ,  title = '2017 Renewed Data')
plt.show()



















