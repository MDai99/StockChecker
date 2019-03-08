# -*- coding: utf-8 -*-
import requests
import time
import winsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import collections

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
print ('This program will keep track of stock levels of popular items')
email = input("Enter your email: ")
password = input("Enter your password: ")
nameList = []
webDict = {}
alreadySent = 0

with open('CheckShops.csv') as mycsv:
    myDict = csv.DictReader(mycsv) #Reads in csv file
    for row in myDict:
        nameList.append(row['Name'])
        webDict[row['Name']] = {}
        webDict[row['Name']]['Link'] = row['Link']
        webDict[row['Name']]['Identifier'] = row['Identifier']
        webDict[row['Name']]['alreadySent'] = 0

while True:
    time.sleep(3) #To prevent being flagged as a bot
    for name in nameList:
        url = webDict[name]['Link']
        htmlContent = requests.get(url, headers=header)
        foundItem = htmlContent.text.find(webDict[name]['Identifier']) #Check for stock
        if foundItem == -1: #Continues beeping
            winsound.Beep(1000, 1000)
        if foundItem == -1 and webDict[name]['alreadySent'] == 0: #If out of stock message is not found, send email
            webDict[name]['alreadySent'] = 1 #To prevent sending too many emails
            print ('ALERT!')
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login(email, password)
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = email
            msg['Subject'] = "FOUND" + name
            s.send_message(msg)
            del msg
