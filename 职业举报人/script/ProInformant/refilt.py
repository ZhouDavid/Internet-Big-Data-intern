#coding:utf-8
import pandas as pd
import numpy as np
import re
import os
import time

def isPro(x):
    if '订单号' in x:
        return True
    return False

d3 = pd.read_csv('out3.csv')
d5 = d3[d3['RECORD_CONTENTS'].map(isPro)]
d5['PROFESSIONAL_PERSON']=1
d5.to_csv('out5.csv',index=False,encoding='gbk')