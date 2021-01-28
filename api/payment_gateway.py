from flask import Flask
from api.payment_process import Validate
import requests, json


class PremiumPaymentGateway:

    def __init__(self, amount):
        self.amount = amount

    def process_premium(self):
        return {
            "status" : "Payment is processed through Premium Payment Gateway",
        }, 200

class CheapPaymentGateway:

    def __init__(self, amount):
        self.amount = amount
    
    def process_cheap(self):
        return {
            "status" : "Payment is processed through Cheap Payment Gateway",
        }, 200

class ExpensivePaymentGateway:
    def __init__(self, amount):
        self.amount = amount
    
    def process_expensive(self):
        return {
            "status" : "Payment is processed through Expensive Payment Gateway",
        }, 200