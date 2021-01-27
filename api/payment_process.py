from flask import Flask, abort, Response
from decimal import Decimal

import datetime
import json

class Validate:

    def __init__(self, CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
        self.CreditCardNumber = CreditCardNumber
        self.CardHolder = CardHolder
        self.ExpirationDate = ExpirationDate
        self.SecurityCode = SecurityCode
        self.Amount = Amount
    
    
    def check_credit_card(self, CreditCardNumber):
        v_sum = 0
        num_digits = len(CreditCardNumber)
        oddeven = num_digits & 1

        if num_digits == 16:
            for count in range(0, num_digits):
                digit = int(CreditCardNumber[count])

                if not ((count & 1) ^ oddeven):
                    digit = digit * 2
                if digit > 9:
                    digit = digit - 9

                v_sum += digit

            if (v_sum % 10) == 0:
                return True
            else:
                return False
        else:
            return False

    def validate_data(self):
        
        if self.CreditCardNumber:
            if type(self.CreditCardNumber) == str:
                response = self.check_credit_card(self.CreditCardNumber)
                if response == False:
                    return {
                        "status" : "Failed",
                        "message" : "Invalid Card Number"
                    }, 400
                else:
                    pass
            else:
                return {
                    "status" : "Failed",
                    "message" : "Invalid Card Number"
                }, 400
        else:
            return {
                "status" : "Failed",
                "message" : "Invalid Card Number"
            }, 400
        
        
        if self.CardHolder:
            if self.CardHolder == "":
                return {
                    "status" : "Failed",
                    "message" : "Please Input a name"
                }, 400
        else:
            return {
                "status" : "Failed",
                "message" : "Please Input a name"
            }, 400
        
        if self.ExpirationDate:
            try:
                date = datetime.datetime.strptime(self.ExpirationDate, "%Y/%m").date()
                if date < datetime.date.today():
                    return {
                        "status" : "Failed",
                        "message" : "This credit card has expired"
                    }, 400

            except ValueError:
                return {
                    "status" : "Failed",
                    "message" : "Invalid Expiration Date"
                }, 400
        else:
            return {
                "status" : "Failed",
                "message" : "Invalid Expiration Date"
            }, 400
        
        if self.SecurityCode:
            if (len(self.SecurityCode) !=3 ) or (type(self.SecurityCode) != str):
                return {
                    "status" : "Failed",
                    "message" : "Invalid Security Code"
                }, 400
        else:
            return {
                "status" : "Failed",
                "message" : "Invalid Security Code"
            }, 400
        
        if self.Amount:
            if self.Amount <= 0:
                return {
                    "status" : "Failed",
                    "message" : "Invalid Amount"
                }, 400
        else:
            return {
                "status" : "Failed",
                "message" : "Invalid Amount"
            }, 400

        return self.Amount