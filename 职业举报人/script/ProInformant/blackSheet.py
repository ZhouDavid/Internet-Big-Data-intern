#coding:utf-8
import os
import pandas as pd
import numpy as np

directory = os.path.join('..','..','..','data','professional informant')
dataPath = os.path.join('..','..','..','data','professional informant','out.csv')
data = pd.read_csv(dataPath,encoding='gbk')
print('data scale:{}'.format(data.shape))

#选出所有职业举报记录
proData = data[data['PROFESSIONAL_PERSON']==1]
print('proData scale:{}'.format(proData.shape))

#统计电话号码频率
gb = proData[['UNID','REPORT_PERSON_MOBILE','REPORT_PERSON_NAME']].groupby(by=['REPORT_PERSON_MOBILE','REPORT_PERSON_NAME'])
print(gb.count())
gb.count().to_csv(os.path.join(directory,'gb.csv'))
