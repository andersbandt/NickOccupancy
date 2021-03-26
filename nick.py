#!/usr/bin/env python
# coding: utf-8

import requests, json, os
from bs4 import BeautifulSoup
import sqlite3
import datetime

url = "https://services.recwell.wisc.edu/FacilityOccupancy"
resp = requests.get(url)
resp.raise_for_status()

doc = BeautifulSoup(resp.text, "html.parser")

strongs = doc.find_all("strong")

value = 0

for i in strongs:
	num = i.get_text().replace("%", "")
	try:
		num = int(num)
		if num <= 100:
			value = num
			break
	except:
		pass


# get the date and time the recording was taken at
date = datetime.datetime.now()


# display some output to the console
print("The current occupancy is ")
print(value)
print("Attempting to connect to occupancy database")

# insert the value into the table
conn = sqlite3.connect('/home/pi/Python/NickOccupancy/data.db')
conn.execute("INSERT INTO OCCUPANCY (DATETIME, OCCUPANCY) \
		VALUES (?, ?)",
		(date, value))

conn.commit()

print("Occupancy level saved successfuly")

conn.close()



