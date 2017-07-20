#coding:utf-8
import pandas as pd
import numpy as np
import os
import time

def extract(data,extractNum):
    return data.iloc[:extractNum]

if __name__ == '__main__':
    startTime = time.time()
    rawDataFileName = os.path.join('..','..','data','smallRawData.csv')
    # print(rawDataFileName)
    rawData = pd.read_csv(rawDataFileName)
    # smallRawData = extract(rawData,3000)
    # smallRawData.to_csv(os.path.join('..','..','data','smallRawData.csv'), index=False)
    # print(rawData.shape)
    columns = rawData.columns
    print(columns[0])
    endTime = time.time()
    print('finished,cost {} seconds'.format(endTime-startTime))