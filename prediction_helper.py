"""
prediction_helper.py

This module contains helper functions used to process applicant input data,
apply feature scaling, run a trained ML classification model to predict 
default probability, and convert the result into a credit score and rating.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Path to the saved model and scaler
MODEL_PATH = 'artifacts/model_data.joblib'

# Load trained model artifacts
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']

def prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                  delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                  residence_type, loan_purpose, loan_type):
    """
    Prepare user input as a DataFrame and scale it for prediction.
    Returns a scaled, feature-aligned DataFrame.
    """

    # Create input dictionary with model-required fields
    input_data = {
        'age': age,
        'loan_tenure_months': loan_tenure_months,
        'number_of_open_accounts': num_open_accounts,
        'credit_utilization_ratio': credit_utilization_ratio,
        'loan_to_income': loan_amount / income if income > 0 else 0,
        'delinquency_ratio': delinquency_ratio,
        'avg_dpd_per_delinquency': avg_dpd_per_delinquency,

        # One-hot encoded categorical features
        'residence_type_Owned': 1 if residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residence_type == 'Rented' else 0,
        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,
        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0,

        # Dummy features (required by scaler/model, not used in logic)
        'number_of_dependants': 1,
        'years_at_current_address': 1,
        'zipcode': 1,
        'sanction_amount': 1,
        'processing_fee': 1,
        'gst': 1,
        'net_disbursement': 1,
        'principal_outstanding': 1,
        'bank_balance_at_application': 1,
        'number_of_closed_accounts': 1,
        'enquiry_count': 1
    }

    # Convert to DataFrame
    df = pd.DataFrame([input_data])

    # Scale relevant columns using fitted scaler
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Align with the exact feature order expected by the model
    df = df[features]

    return df

def calculate_credit_score(input_df, base_score=300, scale_length=600):
    """
    Applies the logistic regression model to predict default probability.
    Converts the result into a credit score (300–900) and assigns a rating.
    """

    # Get raw model output (logits)
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_

    # Convert to default probability using sigmoid
    default_probability = 1 / (1 + np.exp(-x))
    non_default_probability = 1 - default_probability

    # Convert to credit score between 300 and 900
    credit_score = base_score + non_default_probability.flatten() * scale_length

    # Map score to rating category
    def get_rating(score):
        if 300 <= score < 500:
            return 'Poor'
        elif 500 <= score < 650:
            return 'Average'
        elif 650 <= score < 750:
            return 'Good'
        elif 750 <= score <= 900:
            return 'Excellent'
        else:
            return 'Undefined'

    rating = get_rating(credit_score[0])

    return default_probability.flatten()[0], int(credit_score[0]), rating

def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    """
    Wrapper function to:
    - Prepare input
    - Make prediction
    - Return (default probability, credit score, rating)
    """

    input_df = prepare_input(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    probability, credit_score, rating = calculate_credit_score(input_df)

    return probability, credit_score, rating
