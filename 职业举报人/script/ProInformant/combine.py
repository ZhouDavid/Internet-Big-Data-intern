#coding:utf-8
import pandas as pd
import numpy as np

df1 = pd.read_csv('out1.csv',encoding='gbk')
df2 = pd.read_csv('out2.csv',encoding='gbk')
df3 = pd.read_csv('out3.csv',encoding='utf-8')
df4 = pd.read_csv('out4.csv',encoding='gbk')

df = pd.concat([df1,df2,df3,df4])
#df.to_csv('out.csv',index=False,encoding='gbk')
print(df1.shape,df2.shape,df3.shape,df4.shape)
