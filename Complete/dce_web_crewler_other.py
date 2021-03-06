# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:58:27 2017

@author: hyps4
"""

import requests
import time
import pandas as pd
import random
import datetime
from bs4 import BeautifulSoup


url_excel = 'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesData.html'
url_click = 'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html'

#IP池设定
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=20,pool_connections=2)
session.mount('https://', adapter)
session.mount('http://', adapter)

prox = {
        'https':'39.137.69.10:80',
        'https':'39.137.69.8:80'}
          
contract_id=['pp','jm','jd','fb','cs','bb','y','v','p','m','l','j','i','c','a','b']
#contract_id=['y']

for i in range(0,len(contract_id)):
    now_date = datetime.datetime(2018,6,27)
    print(contract_id[i])
    
    while now_date <= datetime.datetime(2018,7,12):
        tmp = now_date
        
        
        split_date = now_date.strftime('%Y-%m-%d').split('-')
        
        formData = {'memberDealPosiQuotes.variety':contract_id[i],
            'memberDealPosiQuotes.trade_type':'0',
            'year':split_date[0],
            'month':str(int(split_date[1])-1),
            'day':str(int(split_date[2])),
            'contract.contract_id': 'all',
            'contract.variety_id':contract_id[i]}
        
        res = requests.post(url_click,data=formData,stream=True,proxies = prox)
        soup = BeautifulSoup(res.text,'lxml')
        click = (soup.findAll('li',{'class':'keyWord_65'}))
        res.close()
        
        for con in click:
            contract_number = con.get_text(strip=True)
            #网站抓取设定
            formData = {'memberDealPosiQuotes.variety':contract_id[i],
                        'memberDealPosiQuotes.trade_type':'0',
                        'year':split_date[0],
                        'month':str(int(split_date[1])-1),
                        'day':str(int(split_date[2])),
                        'contract.contract_id':contract_number,
                        'contract.variety_id':contract_id[i],
                        'exportFlag':'excel'}
            
            res = requests.post(url_excel,data=formData,stream=True)
            res.encoding = 'utf-8-sig'
    
            while(res.status_code != 200):
                res = requests.post(url_excel,data=formData,stream=True) #proxies = prox
                time.sleep(random.randrange(2,5))
    
        
            #存成excel檔 
            with open('../../大商所更新/'+split_date[0]+split_date[1]+split_date[2]+'.xls', 'wb') as file:
                file.write(res.content)
            res.close()
            time.sleep(random.randrange(2,5))
            
            try:
                data = pd.read_excel('../../大商所更新/'+split_date[0]+split_date[1]+split_date[2]+'.xls',encoding='gbk') 
                data.to_csv('../../各交易所期貨持倉量/大商所_分類/'+contract_id[i]+'_o/'+split_date[0]+split_date[1]+split_date[2]+ "_" + contract_number +'.csv',encoding='gbk',index=None)                 
            except Exception as e:
                print(e)
        
        now_date = now_date + datetime.timedelta(days = 1)

