# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 13:00:58 2017

@author: hyps4
"""
import requests
import time
import pandas as pd
import random
import datetime

url = 'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html'

#以下是分期獲取的代碼
# =============================================================================
# for x in range(0,len(date.dropna())):
#     split_date = date['Date'][x].strftime('%Y-%m-%d').split('-')
#     
#     formData = {'memberDealPosiQuotes.variety':'m',
#             'memberDealPosiQuotes.trade_type':'0',
#             'year':split_date[0],
#             'month':str(int(split_date[1])-1),
#             'day':str(int(split_date[2])),
#             'contract.variety_id':'m'} 
#     res = requests.post(url,data=formData,stream=True)
#     soup = BeautifulSoup(res.text,'lxml')
#     click = (soup.findAll('li',{'class':'keyWord_65'}))
#     res.close()
# =============================================================================
    
now_date = datetime.datetime(2017,11,29)

while now_date < datetime.datetime.now():
    split_date = now_date.strftime('%Y-%m-%d').split('-')
    
    try:
        data = pd.read_excel('../大商所更新/'+split_date[0]+split_date[1]+split_date[2]+'.xls',encoding='gbk')                  
    except:
        now_date = now_date + datetime.timedelta(days = 1)
        continue
    data.to_csv('../大商所更新2/'+split_date[0]+split_date[1]+split_date[2]+'.csv',encoding='gbk',index=None)
    now_date = now_date + datetime.timedelta(days = 1)