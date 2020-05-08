#!/usr/bin/env python
from datetime import datetime
from datetime import*
import requests
from bs4 import BeautifulSoup as bsoap
import pickle as pck
import re
import os
import nsepy
import pandas as pd
import numpy as np
from os import path
import shutil
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from nsepy import get_history
from loading_data import ext
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
import os

# open it, go to a website, and get results

ch='d'
k = pd.read_csv('ind_nifty500list.csv')
lg = k.Symbol.unique()
nmlist=[]
month = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sep','Oct','Nov','Dec']
for i in lg:
  
  k1=k[k.Symbol==i]
  if(len(k1)!=0):
   nmlist.append(list(k1[k.columns[-1]])[0])
symlist=nmlist
date1=os.environ.get('DATE1')
date2=os.environ.get('DATE2')
symb = os.environ.get('SYMBOL')
k1 = k[k.Symbol==symb]
symb=list(k1['ISIN Code'])[0]
def dailydata(s,driver,date1,date2):
  def ext_date(datez,month):
      dt=datetime.strptime(datez,'%Y-%m-%d').date()
      day = datez[8:10]
      month = month[int(datez[5:7])-1]
      year = datez[0:4]
      return day,month,year
  day_from,month_from,year_from = ext_date(date1,month)
  day_to,month_to,year_to = ext_date(date2,month)
  print(driver.current_url)
  tbox = driver.find_element_by_xpath('//*[@id="company"]')
  tbox.send_keys(s)
  btxpath =  "div.MT2:nth-child(1) > input:nth-child(2)"
  flag=0
  c=0
  while(flag==0):
      try:
        driver.find_element_by_css_selector(btxpath).click()
        flag=1
      except Exception as e:
        print(e)
        c=c+1
        if(c==3): 
          flag=1
        print('sleeping')
        time.sleep(5)
  print(driver.current_url)
  hpxpath= "Historical Prices"
  flag=0
  c=0
  flag1=0
  while(flag==0):
      try:
        driver.find_element_by_link_text(hpxpath).click()
        flag=1
      except Exception as e:
        print(e)
        c=c+1
        print('sleeping')
        if(c==3):
          flag=1
          flag1=1
        time.sleep(5)
  if(flag1):
    return pd.DataFrame()
  pg = bsoap(driver.page_source,'html.parser')
  driver.get(pg.find('a',title='Click Here')['href'])
  nse1 = Select(driver.find_element_by_css_selector('#ex'))
  if(ch=='d'):
      nse1.select_by_visible_text('NSE')
      nse = Select(driver.find_element_by_name('frm_dy'))
      nse.select_by_visible_text(str(day_from))
      nse = Select(driver.find_element_by_name('frm_mth'))
      nse.select_by_visible_text(str(month_from))
      nse = Select(driver.find_element_by_name('frm_yr'))
      nse.select_by_visible_text(str(year_from))
      nse = Select(driver.find_element_by_name('to_dy'))
      nse.select_by_visible_text(str(day_to))
      nse = Select(driver.find_element_by_name('to_mth'))
      nse.select_by_visible_text(str(month_to))
      nse = Select(driver.find_element_by_name('to_yr'))
      nse.select_by_visible_text(str(year_to))
      p = driver.find_element_by_css_selector('#mc_mainWrapper > div.PA10 > div > div.PT15 > div.PT10 > div.brdb > table > tbody > tr > td:nth-child(1) > form > div:nth-child(4) > input[type="image"]:nth-child(4)')
      p.click()
  else:
      nse =Select(driver.find_element_by_name('mth_frm_mth'))
      nse.select_by_visible_text('Mar')
      nse =Select(driver.find_element_by_name('mth_frm_yr'))
      nse.select_by_visible_text('2000')
      nse =Select(driver.find_element_by_name('mth_to_mth'))
      nse.select_by_visible_text('Mar')
      nse =Select(driver.find_element_by_name('mth_to_yr'))
      nse.select_by_visible_text('2019')
      p = driver.find_element_by_css_selector('td.PT15:nth-child(3) > form:nth-child(1) > div:nth-child(4) > input:nth-child(3)')
      p.click()


  k=[]
  flag=0
  while(True):
     try:
        pg = bsoap(driver.page_source,'html.parser')

        tab = pg.find_all('table',class_='tblchart')[0]
        
        k.append(pd.read_html(str(tab)))        
        #k.append(pd.read_html(driver.current_url,attrs={'class':'tblchart'}))
        #url = str(driver.current_url.encode('ascii'))
        url = driver.current_url
        url = url[0:url.find('?')]
        elem = pg.find_all('a',class_='nextprev')
        flag=1
     
        if(len(elem)==0):
              break
          #    url1 = str(elem[0]['href'].encode('ascii'))

          #url1 = elem[0]['href'].decode('utf-8')
        url1 = elem[0]['href']
        url = url+url1
        driver.get(url)
        print(k)
        print('next')
     except Exception as e:
        print(e)
  
  flag=1
  print(k)
  k =pd.concat(k[0:][0])
  k['id'] = s
  with open('daily_data','a+b') as d:
       pck.dump(k,d)
  driver.quit()
  return k
def driver_act(driver):
  driver.find_element_by_link_text('Financials').click()
  return
def ext_symb(pg):
   sym = pg.find('ctag',class_='mob-hide').text.encode('ascii')
   sym = str(sym)
   bse = re.findall('\d+',sym[sym.find('BSE')+3:])
   nse = re.findall('\w+',sym[sym.find('NSE')+3:])
   return bse,nse
def fin_data(i,driver):
    try:
            print('in here')
            print(driver.current_url)
            driver.find_element_by_xpath('//*[@id="company"]').send_keys(i)
            bt = driver.find_element_by_css_selector('div.MT2:nth-child(1) > input:nth-child(2)')
            bt.click()
            print(driver.current_url)
            ct=0
            while(1):
                if(ct>=3):
                    break
                try:
                 driver_act(driver)
                 break
                except Exception as e:
                 print(e)
                 ct=ct+1
                 time.sleep(10)
            pg1 = bsoap(driver.page_source,'html.parser')
            title = pg1.find('h1',class_='pcstname').text
            rat = pg1.find('a',title='Ratios')
            driver.get(rat['href'])
            bse,nse = ext_symb(pg1)
            flag=0
            flag1=1
            k=[]
            while(flag==0):
                try:
                    print('on')
                    url1 = driver.current_url
                    print(url1)
                    k1 = pd.read_html(url1,header=0)[0]
                    k.append(k1)
                    print(len(k1))
                    k1['title']=title
                    k1['NSE'] = ''
                    k1['BSE']=''
                    if len(bse)!=0: k1['BSE']=bse[0]
                    if len(nse)!=0: k1['NSE']=nse[0]
                    print(nse[0])
                    pg = bsoap(driver.page_source,'html.parser')
                    btx=driver.find_element_by_xpath('//*[@id="mc_content"]/div[2]/div/div[2]/ul/li[2]/a')
                    driver.execute_script("arguments[0].click();", btx)
                    if(driver.current_url.encode('ascii')==url1.encode('ascii')): 
                      print('reach') 
                      flag=1
                except Exception as e:
                    print(e)
                    flag1=0
                    flag=1
            if(flag1==1): 
              k = pd.concat(k,axis=1)
              df=k
              df = df.loc[:,~df.columns.duplicated()]

              ext().store_file('/usr/share/app','finalkfr1',df)
    except Exception as e:
             print(e)
             return
    print(i)
    last_symb = nse[0]
    print(nse[0])
    return k
wd = webdriver.Chrome('/usr/bin/chromedriver',options=options)
wd.get('https://www.moneycontrol.com/india/stockpricequote/')
if(date1=='-'):
    k = fin_data(symb,wd)
else:
    k = dailydata(symb,wd,date1,date2)
#for i in symlist:
#  wd = webdriver.Chrome('/usr/bin/chromedriver',options=options)
#  wd.get('https://www.moneycontrol.com/india/stockpricequote/')
#  dailydata(i,wd)
