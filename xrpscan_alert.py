
import pandas as pd
import requests, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parinya import LINE
import datetime, pytz, time
import pandas as pd
import requests, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parinya import LINE
import datetime, pytz, time
 
os.chdir(r"")

def clean_datetime(df):
    date_time = df['Date'].str[-5:].str.split(':')
    
    for idx, (i, j) in enumerate(date_time):
        i = int(i)
        if i > 23:
            date_time[idx][0] = str(i-24)
            
    for idx, i in enumerate(date_time):
        date_time[idx] = ':'.join(i)
    
    df['Date'] = df['Date'].str[:-5].str.cat(date_time)
    return df

def get_data(driver, url, tags):
    
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div/div[4]/div/div/div/div[2]/div/div/div[2]/ul/li[2]/a/span[1]')))
    
    html = driver.page_source
    
    df = pd.read_html(html)[3]
    
    df['Amount'] = df['Amount'].str.replace('XRP', '')
    df['Amount'] = df['Amount'].str.replace(',', "")
    df['Amount'] = df['Amount'].astype('float64')
    
    df[['To', 'Tag']] = df['To'].str.split('DT:', expand=True)
    df['Tag'] = df['Tag'].str.strip()
    df['To'] = df['To'].str.strip()
    
    
    if df['Date'].str.contains('24:').sum() > 0:
        df['Date'] = df['Date'].str.replace('24:', '00:')
        df['Date'] = pd.to_datetime(df['Date'])
        # df = clean_datetime(df)
        # df['Date'] = pd.to_datetime(df['Date'])
        
    else:
        df['Date'] = pd.to_datetime(df['Date'])
    
    cols = ['Type', 'Date', 'Tx_hash', 'From', 'Flow', 'To', 'Amount', 'NaN', 'Tag']
    df.columns = cols
    
    # Parameters
    
    
    df = df[df['Tag'].isin(tags)]
    df = df.reset_index(drop=True)
    
    return df




# Hyperparameters
url = 'https://xrpscan.com/account/rPFXvVo2fYXVPdV9gCHQouHsMgMhQ2aUwM'
tags = ['2197236416', '102086525']
line = LINE('')

# Algorithm

driver = webdriver.Chrome()


while True:
    try:
        df = get_data(driver, url, tags) 
        
        if len(df) > 0:
            
            df_alert = pd.read_csv(r'.\log\alert_log.csv')
            df_alert['Date'] = pd.to_datetime(df_alert['Date'])
            
            df_min_date = df.loc[df['Date'] == df['Date'].max(), 'Date'].values[0]
            df_alert_min_date = df_alert.loc[df_alert['Date'] == df_alert['Date'].max(), 'Date'].values[0]
            
            

            if df_min_date > df_alert_min_date:
                df = df.loc[df['Date'] > df_alert_min_date, :]
                
                for i in range(len(df)):
                    
                    date = df.loc[i, 'Date'].strftime('%Y-%m-%d %H:%M:%S')
                    flow = df.loc[i, 'Flow']
                    tag = df.loc[i, 'Tag']
                    amount = df.loc[i, 'Amount']
                    
                    line.sendtext(f'\nDate: {date} \
                                   \nFlow: {flow} \
                                   \nTag: {tag} \
                                   \nAmount: {amount}')
                                   
                    print('Sending notification to LINE')
                                   

                df.to_csv(r'.\log\alert_log.csv', index=False, mode='a', header=False)
    
        else:
            pass
        
    except Exception as e:
        
        print("Something wrong, Please checkc errorlog")
        line.sendtext('Something wrong, Please checkc errorlog"')
        
        with open(r".\log\errorlog.txt", "a+") as myfile:
            current_time = datetime.datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M:%S')
            
            myfile.write(f"\n{current_time}")
            myfile.write(f"\nError log: {e}")
            
    
    time.sleep(60)
            
    
