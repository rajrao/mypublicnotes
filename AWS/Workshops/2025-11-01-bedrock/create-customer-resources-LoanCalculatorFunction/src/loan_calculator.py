import json
import logging

def lambda_handler(event, context):
    print (f"event: {event}")
    
    income = get_params_by_name(event, 'income')
    totalDebt = get_params_by_name(event, 'totalDebt')
    loanTerm = get_params_by_name(event, 'loanTerm')
    
    return  calculate_max_loan_affordability (income, totalDebt, loanTerm)

def get_params_by_name(data, name):
    node = data.get('node')
    if node:
        inputs = node.get('inputs')
        if inputs:
            for input_dict in inputs:
                if input_dict.get('name') == name:
                    return input_dict.get('value')
    return None

import logging

def calculate_max_loan_affordability(yearly_income, total_debt, loan_term):
    """
    Calculates the maximum loan affordability based on the given inputs.

    Args:
        yearly_income (float): The applicant's yearly income.
        total_debt (float): The applicant's total debt.
        loan_term (int): The loan term in years.

    Returns:
        int: The maximum loan amount the applicant can afford, rounded to the nearest integer, or 0 if an error occurs.
    """
    try:
        # Calculate monthly income
        monthly_income = yearly_income / 12
        print(f"[Monthly Income] {monthly_income}")

        # Calculate monthly debt payments
        monthly_debt_payments = total_debt / 12
        print(f"[Monthly Debt Payments] {monthly_debt_payments}")

        # Calculate maximum monthly debt-to-income ratio (DTI)
        max_dti = 0.43  # Typical maximum DTI for mortgage loans
        print(f"[Maximum DTI] {max_dti}")

        # Calculate maximum monthly payment based on DTI
        max_monthly_payment = monthly_income * max_dti - monthly_debt_payments
        print(f"[Maximum Monthly Payment] {max_monthly_payment}")

        # Calculate maximum loan amount based on monthly payment and loan term
        interest_rate = 0.05  # Assume a 5% interest rate for simplicity
        monthly_interest_rate = interest_rate / 12
        n = loan_term * 12  # Number of monthly payments
        max_loan_amount = max_monthly_payment * (1 - (1 + monthly_interest_rate) ** (-n)) / monthly_interest_rate
        print(f"[Maximum Loan Amount (Unrounded)] {max_loan_amount}")

        # Ensure the maximum loan amount is not negative
        max_loan_amount = max(0, max_loan_amount)

        # Round the maximum loan amount to the nearest integer
        max_loan_amount = round(max_loan_amount)
        print(f"[Maximum Loan Amount (Rounded)] {max_loan_amount}")

        return max_loan_amount

    except Exception as e:
        # Log the error
        logging.error(f"An error occurred: {e}")
        return 0