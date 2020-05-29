# -*- coding: utf-8 -*-
"""
Created on Wed May 13 00:43:11 2020

@author: petch
"""

from selenium import webdriver
import os
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import pandas as pd   
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pickle

os.chdir("D:\XRP")

driver = webdriver.Chrome()


url_list = [
    # 'https://xrpscan.com/account/rwU8rAiE2eyEPz3sikfbHuqCuiAtdXqa2v'
    # 'https://xrpscan.com/account/rLHtvB1kZimYJsDCqCX4iQxRtSAqqFtrA7',
    # 'https://xrpscan.com/account/rpXTzCuXtjiPDFysxq8uNmtZBe9Xo97JbW',
    # 'https://xrpscan.com/account/rLSn6Z3T8uCxbcd1oxwfGQN1Fdn5CyGujK',
    # 'https://xrpscan.com/account/razRZUaHD9Kojz1AWo936QPq3S1KrnfS9Z',
    # 'https://xrpscan.com/account/rNEBHRf9UYJRVeu6q7qcDV2tM7bM4EDf2B',
    # 'https://xrpscan.com/account/rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh',
    # 'https://xrpscan.com/account/rUzWJkXyEtT8ekSSxkBYPqCvHpngcy6Fks',
    # 'https://xrpscan.com/account/rHfwtjakCgMA7z9AbugfNYV3UvdyugZMr2',
    # 'https://xrpscan.com/account/rLoD9U2ghXP2xUYbtML6G6v1p8LhM9mSnc',
    # 'https://xrpscan.com/account/rLW9gnQo7BQhU6igk5keqYnH3TVrCxGRzm',
    'https://xrpscan.com/account/rDCgaaSBAWYfsxUYhCk1n26Na7x8PQGmkq',
    # 'https://xrpscan.com/account/rfpxubnWte6sSc2uN4w3AzjgGEpo6vHidg',
    # 'https://xrpscan.com/account/rwU8rAiE2eyEPz3sikfbHuqCuiAtdXqa2v'
    ]

url_dict = {}
address_name = [
    # 'AltCoinTrader (1)', 
    # 'Bitkub', 
    # 'Bitso (3)'
    # 'razRZUaHD9Kojz1AWo936QPq3S1KrnfS9Z', 
    # 'rNEBHRf9UYJRVeu6q7qcDV2tM7bM4EDf2B',
    # 'Binance (1)', 
    # 'OKEx', 
    # 'rHfwtjakCgMA7z9AbugfNYV3UvdyugZMr2', 
    # 'rLoD9U2ghXP2xUYbtML6G6v1p8LhM9mSnc',
    # 'Bitfinex (1)',
    'Poloniex (1)',
    # 'rfpxubnWte6sSc2uN4w3AzjgGEpo6vHidg',
    # 'Poloniex (2)',
    ]



for url, name in tqdm(zip(url_list, address_name)):
    # time.sleep(3)
    n = 0
    row_num = 0
    page_num = 0
    
    driver.get(url)
    
    Type = []
    date = []
    Tx_hash = []
    From = []
    Flow = []
    To = []
    Amount = []
    
    while n < 100000:
       
        try:
            
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/ul/li[2]/a')))
        
            table = driver.find_elements_by_class_name('table')[3]
            rows = table.find_elements_by_tag_name('tr')
            
            for i in range(len(rows)):   
            # for i in range(len(rows)): 
                try:
                    columns = rows[i].find_elements_by_tag_name('td')
                    
                    check_date = rows[1].find_elements_by_tag_name('td')
                    check_date = check_date[1].text
                    
                    check_date = pd.Series(check_date)
                    check_date_year = pd.to_datetime(check_date).dt.year
                    check_date_month = pd.to_datetime(check_date).dt.month
                    year = check_date_year.values
                    month =check_date_month.values
                    
                    row_num += 1
                    print(f"total rows: {row_num}")
                    print(month)
                
                except:
                    pass

                    
                if (year <= 2018) &  (year >= 2017) & (month <= 7):
                
                    for j in range(len(columns)):
                        # print(columns[i].text)
                        
                        if j == 0:
                            Type.append(columns[0].text)
                        
                        if j == 1:
                            date.append(columns[1].text)
                        
                        if j == 2:        
                            Tx_hash.append(columns[2].text)
                        
                        if j == 3:
                            From.append(columns[3].text)
                            
                        if j == 4:
                            Flow.append(columns[4].text)
                                  
                        if j == 5:
                            To.append(columns[5].text)
                    
                        if j == 6:
                            Amount.append(columns[6].text)
                        
                        print(columns[1].text)

            button = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div[2]/ul/li[2]/a').click()
            
            page_num += 1
            n += 1
            
            print(f"Total page: {page_num}")
            
        except TimeoutException:
            break

    
    df = pd.DataFrame(zip(Type, date, Tx_hash, From, Flow, To, Amount), 
                      columns = ['Type', 'date', 'tx_hash', 'from', 'flow', 'to', 'amount'])
    
    
    # clean
    df['amount'] = df['amount'].apply(lambda x: x.replace(' XRP', ""))
    df['amount'] = df['amount'].apply(lambda x: x.replace(',', ""))
    df['amount'] = df['amount'].astype('float64')
    
    try:
        df[['to', 'tag']] = df['to'].str.split('DT:', expand=True)
        cols = ['Type', 'date', 'tx_hash', 'from', 'flow', 'to', 'tag', 'amount']
        
    except:
        cols = ['Type', 'date', 'tx_hash', 'from', 'flow', 'to', 'amount']
    
    df = df[cols]
    
    url_dict[name] = df

# =============================================================================
# Save
# =============================================================================
with open('address_poloniex1-20180305' + '.pkl', 'wb') as f:
    pickle.dump(url_dict, f, pickle.HIGHEST_PROTOCOL)

# =============================================================================
# Load
# =============================================================================
# with open('address_poloniex1-20180702' +'.pkl', 'rb') as f:
#       aa = pickle.load(f)
