# -*- coding: utf-8 -*-
import requests
import time
import winsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

print ('This program will keep track of stock levels of popular items')

email = input("Enter your email: ")
password = input("Enter your password: ")

alreadysent = 0

with open('CheckShops.csv') as mycsv:
    myDict = csv.DictReader(mycsv) #Reads in csv file
    while True:
        time.sleep(3) #To prevent being flagged as a bot
        for row in myDict:
            url = row['Link']
            htmlContent = requests.get(url, headers=header)
            foo = htmlContent.text.find(row['Identifier']) #Check for stock
            if foo == -1 and alreadysent == 0: #If out of stock message is not found, send email
                alreadysent = 1 #To prevent sending too many emails
                                
                print ('ALERT!')
                s = smtplib.SMTP(host='smtp.gmail.com', port=587)
                s.starttls()
                s.login(email, password)
                
                msg = MIMEMultipart()
                
                msg['From'] = email
                msg['To'] = email
                msg['Subject'] = "FOUND" + row['Name']
                
                s.send_message(msg)
                
                del msg