# -*- coding: utf-8 -*-
"""
JDX Consulting - Sage export split script, designed to group users into AD groups 
and output the groups as csv files ready for automated ingest
"""
import pandas as pd
import numpy as np



#Config-----------------------------------------------------------------------------------------------------------------------

#define paths
path = 'C:/Users/jay.amin/Pictures/'   #output path
path2 = '//JDX-FS01/HOMEDRIVES$/jay.amin/Desktop/DL data.csv'   # input path
#
#read in csv and save to dataframe
#
#
df = pd.read_csv (r''+path2, encoding = "ISO-8859-1") #for an earlier version of Excel, you may need to use the file extension of 'xls'


#
#define whitelists
#
#
grade_control_list = ['J', 'B', 'C', 'A', 'D', 'E', 'F', 'H', 'Z', 'G', 'X', 'I']
business_control_list = ['HO Support', 'Operational Services', 'Consulting Services', 'Insurance', 'HO Sales']
HR_control_list = ['UK', 'Singapore', 'Hong Kong', 'US', 'Ireland']
location_control_list = ['London', 'Singapore', 'Manchester', 'Hong Kong', 'New York', 'Birmingham', 'Dublin', 'Jacksonville']

#-----------------------------------------------------------------------------------------------------------------------
#replace dataframe column names to remove whitespaces in order make referencing easier
df.rename(columns={'Job Profile Name':'Job_Profile'}, inplace=True)
df.rename(columns={'HR Department':'HR_Department'}, inplace=True)
df.rename(columns={'Full Name':'Full_Name'}, inplace=True)
df.rename(columns={'JDX Email':'Email'}, inplace=True)
name_blacklist=['Recruitment Profile']

df.columns
#
#initialise the lists which will store the combination values found in the input file
#
#
grade_list = []
business_list = []
HR_list = []
location_list = []

exdf = pd.DataFrame() #creates a new dataframe that's empty for exceptions

#fill in the de-duped list for name, location, HR department and buisness departments that we will iterate through
for index, row in df.iterrows():
    if (row[1] in name_blacklist or pd.isnull(row[1])):
        exdf = exdf.append(df[df.Full_Name == row[1]])   
    elif (row[2] not in grade_control_list or pd.isnull(row[2])):
        exdf = exdf.append(df[df.Full_Name == row[1]])
    elif (row[3] not in business_control_list or pd.isnull(row[3])):
        exdf = exdf.append(df[df.Full_Name == row[1]])
    elif (row[4] not in HR_control_list or pd.isnull(row[4])):
        exdf = exdf.append(df[df.Full_Name == row[1]])     
    elif (row[5] not in location_control_list or pd.isnull(row[5])):
        exdf = exdf.append(df[df.Full_Name == row[1]])  
    elif pd.isnull(row[6]):
        exdf = exdf.append(df[df.Full_Name == row[1]])         
   
            
  
    if row[2] not in grade_list and str(row[2]) in grade_control_list:  #row[x] is the value we insert into our lists for this row
        if (row[2]=='I' or row[2]=='H' or row[2]=='G'):
            if 'G-H-I' not in grade_list:
                grade_list.append('G-H-I')
        else:
            grade_list.append(row[2])
    elif str(row[2]) not in grade_control_list:
        print('The following black-listed Role is present in the data:' + str(row[2]))
       
        
    if row[3] not in business_list and str(row[3]) in business_control_list:
        business_list.append(row[3])
    elif str(row[3]) not in business_control_list:
        print('The following black-listed Business Unit is present in the data:' + str(row[3]))
       
        
    if row[4] not in HR_list and str(row[4]) in HR_control_list:
        HR_list.append(row[4])
    elif str(row[4]) not in HR_control_list:
        print('The following black-listed HR Department is present in the data:' + str(row[4]))
        
        
    if row[5] not in location_list and str(row[5]) in location_control_list:
        location_list.append(row[5])
    elif str(row[5]) not in location_control_list:
        print('The following black-listed Location is present in the data:' + str(row[5]))

#
#Remove blacklisted rows from dataframe
#
df=df[~df.Full_Name.isin(exdf.Full_Name)]


#Iterate over Job Role - Location combinations and produce a csv
grade_index = 0
business_index = 0
HR_index = 0
df['Alias'] = df['Full_Name'].copy()
for i in grade_list:
    location_index = 0
    for j in location_list:
        newdf = df[(df.Location == location_list[location_index]) & (df.Job_Profile == grade_list[grade_index])]       
        newdf2=newdf[['Full_Name','Alias','Email']]
        newdf2.columns = ['DisplayName', 'Alias', 'PrimarySmtpAddress']
        if len(newdf2)>0:  #check to see if dataframe is empty
            newdf2.to_csv(r''+path+grade_list[grade_index]+"-" + location_list[location_index] + ".csv", index=False)
        if location_index < (len(location_list)-1): # uneccessarry if but included to help debug an index error
            location_index +=1
    if grade_index < (len(grade_list)-1): # uneccessarry but included to help debug an index error
        grade_index+=1




#Iterate over Business Unit - HR combinations and produce a csv
grade_index = 0
business_index = 0
location_index = 0

for i in business_list:
    HR_index = 0
    for j in HR_list:
        newdf = df[(df.HR_Department == HR_list[HR_index]) & (df.Business == business_list[business_index])]       
        newdf2=newdf[['Full_Name','Alias','Email']]
        newdf2.columns = ['DisplayName', 'Alias', 'PrimarySmtpAddress']
        if len(newdf2)>0:
            newdf2.to_csv(r''+path+HR_list[HR_index]+"-"+business_list[business_index]+".csv", index=False)
        if HR_index < (len(HR_list)-1):
            HR_index +=1
    if business_index < (len(business_list)-1):
        business_index+=1






#Iterate over Job Role - business unit combinations and produce a csv
grade_index = 0
location_index = 0
HR_index = 0

for i in grade_list:
    business_index = 0
    for j in business_list:
        newdf = df[(df.Business == business_list[business_index]) & (df.Job_Profile == grade_list[grade_index])]       
        newdf2=newdf[['Full_Name','Alias','Email']]
        newdf2.columns = ['DisplayName', 'Alias', 'PrimarySmtpAddress']
        if len(newdf2)>0:
            newdf2.to_csv(r''+path + grade_list[grade_index] + "-" + business_list[business_index] + ".csv", index=False)
        if business_index < (len(business_list)-1):
            business_index +=1
    if grade_index < (len(grade_list)-1):
        grade_index+=1

#Output validation failures to an exceptions file
exdf.to_csv(r''+path + "exceptions.csv", index=False)






