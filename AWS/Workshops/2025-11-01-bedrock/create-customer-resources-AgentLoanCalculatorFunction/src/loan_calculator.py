import os
import boto3
import decimal


# DynamoDB boto3 resource and variable
dynamodb = boto3.resource('dynamodb',region_name=os.environ['AWS_REGION'])

def get_named_parameter(event, name):
    try:
        return next(item for item in event['parameters'] if item['name'] == name)['value']
    except (KeyError, StopIteration):
        return None

def get_named_property(event, name):
  try:
    return next(item for item in event['requestBody']['content']['application/json']['properties'] if item['name'] == name)['value']
  except (KeyError, StopIteration):
    return None



def calculate_max_loan_affordability(event):
    # collect information like Monthly income, Monthly expenses, Down payment amount and Desired loan term from the event object
    monthly_income = get_named_property(event, 'monthlyIncome')
    monthly_expenses = get_named_property(event, 'monthlyExpenses')
    down_payment = get_named_property(event, 'downPayment')
    loan_term = get_named_property(event, 'loanTerm')
    # check if any of the required information is missing and the return a response that the paramter is missing
    if not monthly_income or not monthly_expenses or not down_payment or not loan_term:
        return {
            "response": "A required parameter is missing"
        }
    # TODO: Include defencive code here to add validation on the inputs to check they are a valid type/range
    # Calculate Monthly Disposable Income using the logic Disposable Income = Monthly Income - Monthly Expenses
    monthly_disposable_income = decimal.Decimal(monthly_income) - decimal.Decimal(monthly_expenses)

    # Calculate Debt-to-income ratio using the logic Debt-to-income ratio = (Monthly Expenses / Monthly Income) * 100
    debt_to_income_ratio = decimal.Decimal(monthly_expenses) / decimal.Decimal(monthly_income) * 100

    # calculate Estimate Maximum Loan Amount: Maximum Loan Payment = Disposable Income * (1 - DTI / 100)
    max_loan_amount = decimal.Decimal(monthly_disposable_income) * (1 - debt_to_income_ratio / 100)

    # Include interest rate and loan terms: Loan Amount = Maximum Loan Payment * [(1 - (1 + Monthly Interest Rate)^(-Number of Monthly Payments))] / Monthly Interest Rate
    monthly_interest_rate = decimal.Decimal(0.05)/12 # assuming 5% interest rate
    monthly_payments = decimal.Decimal(loan_term) * 12
    loan_amount = max_loan_amount * (1 - (1 + monthly_interest_rate)**(-monthly_payments)) / monthly_interest_rate
    
    # Calculate Maximum Loan Affordability using the logic Maximum Loan Affordability = Loan Amount - Down Payment
    max_loan_affordable = loan_amount - decimal.Decimal(down_payment)
    response = {
           "monthly_disposable_income": f"{monthly_disposable_income:,.2f}",
           "debt_to_income_ratio": f"{debt_to_income_ratio:,.2f}",
           "max_monthly_payment": f"{max_loan_amount:,.2f}",
           "total_loan_amount": f"{loan_amount:,.2f}",
           "max_loan_affordable": f"{max_loan_affordable:,.2f}"
        }
    description = '''
    Calculate Monthly Disposable Income using the logic [Disposable Income = Monthly Income - Monthly Expenses.].  
    Calculate Debt-to-income ratio using the logic Debt-to-income ratio = (Monthly Expenses / Monthly Income) * 100. 
    calculate Estimate Maximum Loan Amount: Maximum Loan Payment = Disposable Income * (1 - DTI / 100)
    Include interest rate and loan terms: Loan Amount = Maximum Loan Payment * [(1 - (1 + Monthly Interest Rate)^(-Number of Monthly Payments))] / Monthly Interest Rate
    Calculate Maximum Loan Affordability using the logic Maximum Loan Affordability = Loan Amount - Down Payment
    '''
    return {
        "response":  [response],
        "description": description 
    }


def lambda_handler(event, context):
    response_code = 200
    action_group = event['actionGroup']
    api_path = event['apiPath']
    
    # API path routing
    if api_path == '/loan-affordability-calculator':
        body = calculate_max_loan_affordability(event)
    else:
        response_code = 400
        body = {"{}::{} is not a valid api, try another one.".format(action_group, api_path)}

    response_body = {
        'application/json': {
            'body': str(body)
        }
    }
    
    # Bedrock action group response format
    action_response = {
        "messageVersion": "1.0",
        "response": {
            'actionGroup': action_group,
            'apiPath': api_path,
            'httpMethod': event['httpMethod'],
            'httpStatusCode': response_code,
            'responseBody': response_body
        }
    }
 
    return action_response