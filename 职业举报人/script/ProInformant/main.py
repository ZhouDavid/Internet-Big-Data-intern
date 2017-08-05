#coding:utf-8
import pandas as pd
import numpy as np
import re
import os
import time

#lawRegx = ((\\w|\\W|[\\u4e00-\\u9fa5])*《[\\u4e00-\\u9fa5]]*规定》)*|

def extract(data,extractNum):
    return data.iloc[:extractNum]

def inValid(x):
    if isinstance(x,str):
        if x.startswith('无效举报'):
            return False
    return True

def isPro(x):
    if isinstance(x,str):
        if x.startswith('本人') or '订单号' in x or '诱导我与其交易' in x:
            return True
    return False

def hasLaw(x):
    if '法》' in x or '规定》' in x or '号文' in x:
        return True
    return False

if __name__ == '__main__':
    startTime = time.time()
    rawDataFileName = os.path.join('..','..','..','data','professional informant','commonTest.csv')
    colFileName = os.path.join('..','..','..','data','professional informant','20170501-职业举报人.csv')
    colData = pd.read_csv(colFileName)
    outColNames = colData.columns

    rawData = pd.read_csv(rawDataFileName)
    print('initial shape:{}'.format(rawData.shape))

    inColNames = rawData.columns

    filtData = rawData[(rawData['RECORD_IS_INVALID']==0)&\
                       (rawData['RECORD_TYPE']!=3)]
                      # (rawData['HANDLE_STATE']!=3)
                      # (rawData['REPLY_CONTENTS'].map(inValid))&\
                      #  rawData['HANDLE_RESULT'].map(inValid)&\
                      #  rawData['RECORD_HANDLE_DEVISECONTENTS'].map(inValid)]

    #构建输出数据
    #求colName并集
    newColNames= list(set(outColNames)^(set(inColNames)))
    newColNames = [col for col in newColNames if col in outColNames]
    for col in newColNames:
        filtData[col]=np.nan

    filtData = filtData.reset_index(level = list(range(filtData.shape[0])))

    for i in range(filtData.shape[0]):
        a = filtData.loc[i,'RECORD_CONTENTS']
        if isPro(a):
            filtData.loc[i,'PROFESSIONAL_PERSON'] = 1
        else:
            filtData.loc[i,'PROFESSIONAL_PERSON'] = 0
        if hasLaw(a):
            filtData.loc[i,'RECORD_INCLUDE_LAW'] = 1
        else:
            filtData.loc[i,'RECORD_INCLUDE_LAW'] = 0

    filtData = filtData[outColNames]

    print('filt shape:{}'.format(filtData.shape))
    # 将初步标注好的数据分成四部分：（1，1） （0，1）（0，0） （1，0）
    d1 = filtData[(filtData['PROFESSIONAL_PERSON'] == 1) & (filtData['RECORD_INCLUDE_LAW'] == 1)]
    d2 = filtData[(filtData['PROFESSIONAL_PERSON'] == 1) & (filtData['RECORD_INCLUDE_LAW'] == 0)]
    d3 = filtData[(filtData['PROFESSIONAL_PERSON'] == 0) & (filtData['RECORD_INCLUDE_LAW'] == 1)]
    d4 = filtData[(filtData['PROFESSIONAL_PERSON'] == 0) & (filtData['RECORD_INCLUDE_LAW'] == 0)]

    outDirectory = os.path.join('..','..','..','data','professional informant')
    # d1.to_csv(os.path.join(outDirectory,'out11.csv'), index=False)
    # d2.to_csv(os.path.join(outDirectory,'out10.csv'), index=False)
    # d3.to_csv(os.path.join(outDirectory,'out01.csv'), index=False)
    # d4.to_csv(os.path.join(outDirectory,'out00.csv'), index=False)
    filtData.to_csv(os.path.join(outDirectory,'outTest.csv'),index=False)

    print('split shape:{},{},{},{}'.format(d1.shape,d2.shape,d3.shape,d4.shape))
    endTime = time.time()
    print('finished,cost {} seconds'.format(endTime-startTime))