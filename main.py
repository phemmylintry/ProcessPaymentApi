from flask import Flask, abort
from flask_restful import Resource, Api, reqparse
from flask_swagger_ui import get_swaggerui_blueprint

from api.payment_process import Validate
from api.payment_gateway import PremiumPaymentGateway, CheapPaymentGateway, ExpensivePaymentGateway

app = Flask(__name__)
api = Api(app)


SWAGGER_URL = ''
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Process Payment Gateway"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


parser = reqparse.RequestParser()
parser.add_argument("CreditCardNumber", type=str, help="Please input correct card number", required=True)
parser.add_argument("CardHolder", type=str, help="Please input card holder name", required=True)
parser.add_argument("ExpirationDate", type=str, help="Input expiration date on card, format YYYY/MM", required=True)
parser.add_argument("SecurityCode", type=str)
parser.add_argument("Amount", type=int, required=True)

class Hello(Resource):

    def get(self):
        return {"message" : "Welcome to Process Payment Gateway. Make requests to /processpayment endpoint"}

class ProcessPaymentResource(Resource):

    def post(self):
        args = parser.parse_args(strict=True)
        
        premium = PremiumPaymentGateway
        cheap = CheapPaymentGateway
        expensive = ExpensivePaymentGateway

        processpayment = Validate(
            args.CreditCardNumber,
            args.CardHolder,
            args.ExpirationDate,
            args.SecurityCode,
            args.Amount
        )

        validate = processpayment.validate_data()

        if type(validate) is int:
            if validate > 500:
                response = premium.process_premium(validate)
            elif validate <= 20:
                response = cheap.process_cheap(validate)
            elif validate > 20 and validate <= 500:
                response = expensive.process_expensive(validate)
            return response
        else:
            return validate


api.add_resource(Hello, '/home')
api.add_resource(ProcessPaymentResource, '/processpayment')


if __name__ == '__main__':
    app.run(debug=True)