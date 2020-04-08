#!/usr/bin/env python
# coding: utf-8

# # Analytics employee attrition and perfomance
# 
# 
# ## I .Dataset description
# 
# Uncover the factors that lead to employee attrition and explore important questions such as show me a breakdown of distance from home by job role and attrition or compare average monthly income by education and attrition . Test age, gender, affect attrition .
# 
# #### 1.Age(number)
# #### 2.Attrition (category)
# + yes
# + no
# #### 3.BusinessTravel(category)
# + Non-Travel
# + Travel Rately
# + Travel Frequently
# #### 4.DailyRate(number)
# #### 5.Department(category)
# + Sale
# + Research&Development
# + Human Resources
# #### 6.DistanceFromHome(number)
# #### 7.Education(number from 1 to 4)
# #### 8.EducationField(category)
# + Life Sciences
# + Other
# + Medical
# + arketing
# + Technical Degree
# + man Resources
# #### 9.EmployeeCount (number same =1) .....
# 
# ## II.Data

# In[36]:


import pandas as pd
import numpy as np
import random
from scipy import stats
from scipy.stats import ttest_ind
Data=pd.read_csv("Data.csv")
print(Data)


# ### Comment :
# 
# + Data can be number or category
# + There are columns with one same value > not playing into with columns other
# 

# ## III. Handle missing value
# .....
# 

# ## IV. Analysis data

# In[37]:


def number_or_category(Data_test):
    try:
        try_=Data_test+1
    except:
        Data_type="category"
    else:
        Data_type="number"
    return (Data_type)


# In[38]:


# target have type là number and feature have type category
def Xuly_T_test(Data,feature,target,STT,HT):
    # Tính số thuộc tính trong feature example BusinessTravel have 3 tt là Non-Travel,Travel Rately and Travel Frequently
    feature_set=set(Data[feature]) # convert set{} to remove thuộc tính  same
    #print(feature_set)
    so_thuoc_tinh_feature=len(feature_set)
    #print(so_thuoc_tinh_feature)
    if so_thuoc_tinh_feature==1:
        print(STT," .",feature + " are not playing into current " + target + " Rate")
    else:
        # tách data của target theo từng thuộc tính trong feature
        sample=[]
        not_32=0
        for thuoc_tinh in feature_set:
            row=(Data[Data[feature]==thuoc_tinh].index)
            po_target=list(Data[target][row])
            try:
                take_32=random.sample(po_target,k=32)
            except:
                print(STT," .","Data of ",feature,"not enough 32 for one properties")
                not_32=1
                break
            else:
                sample.append(take_32)
        #print(sample)
        if len(sample) ==2 and not_32==0:
            f,p=stats.ttest_ind(sample[0],sample[1])
            if p< 0.05:
                if HT ==1:
                    print(STT," .",target + " are playing into current " + feature + " Rate" " :  ",(1-p)*100,"%")
                else: 
                    print(STT," .",feature + " are playing into current " + target + " Rate" " :  ",(1-p)*100,"%")
            else :
                if HT ==1:
                    print(STT," .",target + " are not playing into current " + feature + " Rate" " :  ",(1-p)*100,"%")
                else:
                    print(STT," .",feature + " are not playing into current " + target + " Rate" " :  ",(1-p)*100,"%")
        if len(sample) > 2 and not_32==0:# có nhiều hơn 2 thuộc tính xét các cặp nếu 1 cặp khác nhau thì khác nhau
            khac=0
            for i in range(len(sample)-1):
                f,p=stats. f_oneway(sample[i],sample[i+1])
                if p <0.05:
                    khac=1
                    break
            if khac==1:
                if HT ==1:
                    print(STT," .",target + " are playing into current " + feature + " Rate" " :  ",(1-p)*100,"%")
                else: 
                    print(STT," .",feature + " are playing into current " + target + " Rate" " :  ",(1-p)*100,"%")
            else :
                if HT ==1:
                    print(STT," .",target + " are not playing into current " + feature + " Rate" " :  ",(1-p)*100,"%")
                else:
                    print(STT," .",feature + " are not playing into current " + target + " Rate" " :  ",(1-p)*100,"%")


# In[39]:


# Dùng Correlation để xử lý target là number và feature là number 
def Xuly_Correlation(Data,feature,target,STT):
    # lấy random 50 data của feature và của target
    
    sample_feature=random.sample(list(Data[feature]),k=50)
    sample_target=random.sample(list(Data[target]),k=50)
    r,p=stats.pearsonr(sample_feature, sample_target)
    #print(r,p)
    if abs(r) >= 0.5 :
        print(STT," .",feature + " are playing into current " + target + " Rate" " with r = ",r)  
    else:
        print(STT," .",feature + " are not playing into current " + target + " Rate" " with r = ",r)
        
        


# In[40]:


# input data type file.csv
Data=pd.read_csv("Data.csv")
#print(Data.shape)
#print(Data.head(1))
def main_(Data,target):
    target_type=number_or_category(Data[target][0])
    #print("Target có dạng ",target_type)
    STT=0
    for col in range(Data.shape[1]):
        if Data.columns[col] !=target:
            feature=Data.columns[col]
            feature_type=number_or_category(Data.iloc[0][col])
            #print(feature_type)
            if target_type=="number" and feature_type == "number":
                Xuly_Correlation(Data,feature,target,STT)
            if target_type=="number" and feature_type == "category":
                Xuly_T_test(Data,feature,target,STT,0)
            if target_type=="category" and feature_type == "number":
                #Reverve H0
                Xuly_T_test(Data,target,feature,STT,1)
            if target_type=="category" and feature_type == "category":
                # convert  target to binary
                #thuộc tính đầu tiên của target đưa về 0 còn lại đưa về 1(với attrition có 2 thuộc tính là yes và no)
                #nếu chỉ có 1 thuộc tính thì đều chuyển =0  > sẽ không ảnh hưởng và p=nan %
                target_set=list(set(Data[target]))
                thuoc_tinh0=target_set[0]
                # lấy row có thuộc tính ==thuoc_tinh0
                row=list(Data[Data[target]==thuoc_tinh0].index)
                #print(row)
                Data_binary=Data
                #print(Data_binary)
                #chuyển tất cả các data của target =1
                Data_binary[target]=1
                #chuyển các data của target có thuoc_tinh0=0
                for r in row:
                    Data_binary[target].loc[r]=0
                #print(Data_binary)
                # target có dạng number và feature có dang category
                Xuly_T_test(Data_binary,feature,target,STT,0)
        STT+=1


# In[41]:


print("What are key factors that are playing into current attrition Rate ?")      
main_(Data,"Attrition")    
print("What are key factors that are playing into current JobSatisfaction rates ?")
main_(Data,"JobSatisfaction")
print("What are key factors that are playing into current EnvironmentSatisfaction rates ?")
main_(Data,"EnvironmentSatisfaction")
print("What are key factors that are playing into current RelationshipSatisfaction rates ?")
main_(Data,"RelationshipSatisfaction")
            


# In[ ]:




