import unittest
import json
import sys
from main import app
from api.payment_process import Validate

url = 'http://127.0.0.1:5000/processpayment'
class ProcessPaymentTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    
    #1
    def test_credit_card_number_length(self):
        #input an invalid credit card with less digits
        payload = {
            "CreditCardNumber" : "53998302441673",
            "CardHolder": "Femi Adenuga",
            "ExpirationDate": "2020/11",
            "SecurityCode" : "266",
            "Amount" : "501"
        }
        response = self.app.post(url, json=payload)
        exp_response = {
                "status" : "Failed",
                "message" : "Invalid Card Number"
            }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.get_json(), exp_response)
    
    #2
    def test_credit_card_number_is_valid(self):

        """input an invalid credit card with wrong combination, 
        this test will fail the check_credit_card method in Validate class
        """

        payload = {
            "CreditCardNumber" : "5499530644063473",
            "CardHolder": "Femi Adenuga",
            "ExpirationDate": "2020/11",
            "SecurityCode" : "266",
            "Amount" : "501"
        }
        response = self.app.post(url, json=payload)
        exp_response = {
                "status" : "Failed",
                "message" : "Invalid Card Number"
            }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.get_json(), exp_response)
    
    #3
    def test_credit_card_number_field_if_empty(self):

        """Test to check if credit card is empty
        """

        payload = {
            "CreditCardNumber" : "",
            "CardHolder": "John Doe",
            "ExpirationDate": "2020/11",
            "SecurityCode" : "266",
            "Amount" : "501"
        }
        response = self.app.post(url, json=payload)
        exp_response = {
                "status" : "Failed",
                "message" : "Invalid Card Number"
            }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.get_json(), exp_response)
    
    #4
    def test_card_holder_if_empty_field(self):

        """Test to check if card holer field is empty card is empty
        """

        payload = {
            "CreditCardNumber" : "5110073926575583",
            "CardHolder": "",
            "ExpirationDate": "2020/11",
            "SecurityCode" : "266",
            "Amount" : "501"
        }
        response = self.app.post(url, json=payload)
        exp_response = {
                "status" : "Failed",
                "message" : "Please Input a name"
            }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.get_json(), exp_response)
    
    #5
    def test_expiration_date_if_empty_field(self):

        """Test to check if card holer field is empty card is empty
        """

        payload = {
            "CreditCardNumber" : "5110073926575583",
            "CardHolder": "John Doe",
            "ExpirationDate": "",
            "SecurityCode" : "266",
            "Amount" : "501"
        }
        response = self.app.post(url, json=payload)
        exp_response = {
                "status" : "Failed",
                "message" : "Invalid Expiration Date"
            }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.get_json(), exp_response)

    #6
    def test_expiration_date_if_less_than_current_date(self):

        """Test to check if card holer field is empty card is empty
        """

        payload = {
            "CreditCardNumber" : "5110073926575583",
            "CardHolder": "John Doe",
            "ExpirationDate": "2020/11",
            "SecurityCode" : "266",
            "Amount" : "501"
        }
        response = self.app.post(url, json=payload)
        exp_response = {
                "status" : "Failed",
                "message" : "This credit card has expired"
            }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.get_json(), exp_response)
    
    

if __name__ ==  "__main__":
    unittest.main()
