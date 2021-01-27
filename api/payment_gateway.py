from flask import Flask
from api.payment_process import Validate
import requests, json


class PremiumPaymentGateway:

    def __init__(self, amount):
        self.amount = amount

    def process_premium(self):
        url = 'https://sms-microapi.herokuapp.com/v2/sms/user_register'
        payload = {
            "senderID": "testttuiopkjhgfd"
            }

        count = 0
        while count < 3:
            print("hello")
            user = requests.post(url, payload)
            created = user.json()
            response = created["status"]
            
            if response == 400:
                check = True
                count += 1
                print(count)
            else:
                return {
                    "status" : "Payment is processed through P",
                }, 200
            
        return {
            "status" : "Payment is processed through P",
        }, 400

class CheapPaymentGateway:

    def __init__(self, amount):
        self.amount = amount
    
    def process_cheap(self):
        return {
            "status" : "Payment is processed through C",
        }, 200

class ExpensivePaymentGateway:
    def __init__(self, amount):
        self.amount = amount
        print(amount)
    
    def process_expensive(self):
        url = 'https://sms-microapi.herokuapp.com/v2/sms/user_register'
        url = 'https://sms-microapi.herokuapp.com/v2/sms/user_register'
        payload = {
            "senderID": "testtnkljgyjgllkpt"
            }

        count = 0
        while count < 1:
            print("hello")
            user = requests.post(url, payload)
            created = user.json()
            response = created["status"]
            
            if response == 400:
                count += 1
                print("I dey here")
                value = self.amount
                print(value)
                int_value = int(value)
                CheapPaymentGateway.process_cheap(int_value)
            
        return {
            "status" : "Payment is processed through E",
        }, 400

        
        # return {
        #     "status" : "Payment is processed through E",
        # }, 200