#!/usr/bin/env python
# coding: utf-8

# In[3]:

import requests, json, os
from bs4 import BeautifulSoup


url = "https://services.recwell.wisc.edu/FacilityOccupancy"
resp = requests.get(url)
resp.raise_for_status()

doc = BeautifulSoup(resp.text, "html.parser")


strongs = doc.find_all("strong")
for i in strongs:
    num = i.get_text().replace("%", "")
    try:
        num = int(num)
        if num<=100:
            value = num
            break
    except:
        pass
    
