#coding:utf-8
import pandas as pd
import numpy as np
import os
import time

def extract(data,extractNum):
    return data.iloc[:extractNum]

def inValid(x):
    if isinstance(x,str):
        if x.startswith('无效举报'):
            return False
    return True

def isPro(x):
    if isinstance(x,str):
        if x.startswith('本人'):
            return True
if __name__ == '__main__':
    startTime = time.time()
    rawDataFileName = os.path.join('..','..','..','data','professional informant','20170501.csv')
    colFileName = os.path.join('..','..','..','data','professional informant','20170501-职业举报人.csv')
    colData = pd.read_csv(colFileName)
    colNames = colData.columns
    print(colNames)
    # print(rawDataFileName)
    rawData = pd.read_csv(rawDataFileName)
    # smallRawData = extract(rawData,3000)
    # smallRawData.to_csv(os.path.join('..','..','data','smallRawData.csv'), index=False)
    # print(rawData.shape)

    filtData = rawData[(rawData['RECORD_IS_INVALID']==0)&\
                       (rawData['RECORD_TYPE']!=3)&\
                       (rawData['HANDLE_STATE']!=3)&\
                       (rawData['REPLY_CONTENTS'].map(inValid))&\
                        rawData['HANDLE_RESULT'].map(inValid)&\
                        rawData['RECORD_HANDLE_DEVISECONTENTS'].map(inValid)]

    filtData.RECORD_CONTENTS
    print(filtData.shape)
    outputFileName = os.path.join('..','..','..','data','professional informant','out.csv')
    filtData.to_csv('tmp2.csv',index=False)

    endTime = time.time()
    print('finished,cost {} seconds'.format(endTime-startTime))