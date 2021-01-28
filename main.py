from flask import Flask, abort
from flask_restful import Resource, Api, reqparse
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from apispec import APISpec 
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from marshmallow import Schema, fields

from api.payment_process import Validate
from api.payment_gateway import PremiumPaymentGateway, CheapPaymentGateway, ExpensivePaymentGateway

app = Flask(__name__)
api = Api(app)

class ResponseSchema(Schema):
    message = fields.Str(default='Sucess')

class RequestSchema(Schema):
    api_type = fields.String(required=True, description="API type of payment")

parser = reqparse.RequestParser()
parser.add_argument("CreditCardNumber", type=str, help="Please input correct card number", required=True)
parser.add_argument("CardHolder", type=str, help="Please input card holder name", required=True)
parser.add_argument("ExpirationDate", type=str, help="Input expiration date on card, format YYYY/MM", required=True)
parser.add_argument("SecurityCode", type=str)
parser.add_argument("Amount", type=int, required=True)

class Hello(MethodResource,Resource):

    @doc(description='Hompage', tags=['Hello'])
    @marshal_with(ResponseSchema)

    def get(self):
        return {"message" : "Welcome to Process Payment Gateway"}

@marshal_with(ResponseSchema)
class ProcessPaymentResource(MethodResource, Resource):

    @doc(description='Process payment with different payment gateways', tags=['Process Payment'])
    @use_kwargs({
        "CreditCardNumber" : fields.Str(),
        "CardHolder": fields.Str(),
        "ExpirationDate": fields.Str(),
        "SecurityCode" : fields.Str(),
        "Amount" : fields.Str()
    })  # marshalling

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


api.add_resource(Hello, '/hello')
api.add_resource(ProcessPaymentResource, '/processpayment')

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Payment Process Gateway',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/json/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

docs.register(Hello)
docs.register(ProcessPaymentResource)


if __name__ == '__main__':
    app.run(debug=True)