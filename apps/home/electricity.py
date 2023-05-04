import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
from statsmodels.tools.eval_measures import rmse
import matplotlib.pyplot as plt
import os

def get_predicted_kwh(building):
    # load the data
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "electricity.csv"))
    df = pd.read_csv(file_path)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%Y")


    # Set 'Date' column as the index
    df.set_index('Date', inplace=True)
    df.index.freq = pd.infer_freq(df.index)

    # create a dataframe with only the required columns (KwH, max_temp, min_temp)
    df = df[[building, 'MaxTemperature', 'MinTemperature']]

    # split the data into train and test sets (use the last 60 rows for testing)
    train = df[:-30]
    test = df[-30:]

    # fit the VAR model
    model = VAR(train)
    results = model.fit()

    # create lagged values for the test data
    lags = results.k_ar
    test_data = test.values
    history = train.values[train.shape[0]-lags:]
    predictions = []

    # forecast for the test data
    for t in range(test_data.shape[0]):
        model_input = history[-lags:]
        yhat = results.forecast(model_input, steps=1)
        predictions.append(yhat[0])
        history = np.vstack([history, test_data[t]])

    # create a dataframe of predictions and actual values
    pred_df = pd.DataFrame(predictions, index=test.index, columns=df.columns)
    actual_df = test

    # get the predicted values as a list of dictionaries
    predicted_kwh = pred_df[building].reset_index().to_dict('records')


    # return the predicted values
    return predicted_kwh

def get_actual_kwh(building):
    # load the data
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "electricity.csv"))
    df = pd.read_csv(file_path)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%Y")


    # Set 'Date' column as the index
    df.set_index('Date', inplace=True)
    df.index.freq = pd.infer_freq(df.index)

    # create a dataframe with only the required columns (KwH, max_temp, min_temp)
    df = df[[building, 'MaxTemperature', 'MinTemperature']]

    # split the data into train and test sets (use the last 60 rows for testing)
    test = df[-30:]

    # create a dataframe of predictions and actual values
    actual_df = test

    # get the predicted values as a list of dictionaries
    actual_kwh = actual_df[building].reset_index().to_dict('records')


    # return the predicted values
    return actual_kwh

def get_predicted_liter(building):
    # load the data
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "water.csv"))
    df = pd.read_csv(file_path)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%Y")


    # Set 'Date' column as the index
    df.set_index('Date', inplace=True)
    df.index.freq = pd.infer_freq(df.index)

    # create a dataframe with only the required columns (KwH, max_temp, min_temp)
    df = df[[building, 'MaxTemperature', 'MinTemperature']]

    # split the data into train and test sets (use the last 60 rows for testing)
    train = df[:-30]
    test = df[-30:]

    # fit the VAR model
    model = VAR(train)
    results = model.fit()

    # create lagged values for the test data
    lags = results.k_ar
    test_data = test.values
    history = train.values[train.shape[0]-lags:]
    predictions = []

    # forecast for the test data
    for t in range(test_data.shape[0]):
        model_input = history[-lags:]
        yhat = results.forecast(model_input, steps=1)
        predictions.append(yhat[0])
        history = np.vstack([history, test_data[t]])

    # create a dataframe of predictions and actual values
    pred_df = pd.DataFrame(predictions, index=test.index, columns=df.columns)
    actual_df = test

    # get the predicted values as a list of dictionaries
    predicted_liter = pred_df[building].reset_index().to_dict('records')


    # return the predicted values
    return predicted_liter

def get_actual_liter(building):
    # load the data
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "water.csv"))
    df = pd.read_csv(file_path)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%Y")


    # Set 'Date' column as the index
    df.set_index('Date', inplace=True)
    df.index.freq = pd.infer_freq(df.index)

    # create a dataframe with only the required columns (KwH, max_temp, min_temp)
    df = df[[building, 'MaxTemperature', 'MinTemperature']]

    # split the data into train and test sets (use the last 60 rows for testing)
    test = df[-30:]

    # create a dataframe of predictions and actual values
    actual_df = test

    # get the predicted values as a list of dictionaries
    actual_liter = actual_df[building].reset_index().to_dict('records')


    # return the predicted values
    return actual_liter

def get_predicted_cf(building):
    # load the data
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cf.csv"))
    df = pd.read_csv(file_path)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%Y")


    # Set 'Date' column as the index
    df.set_index('Date', inplace=True)
    df.index.freq = pd.infer_freq(df.index)

    # create a dataframe with only the required columns (KwH, max_temp, min_temp)
    df = df[[building, 'MaxTemperature', 'MinTemperature']]

    # split the data into train and test sets (use the last 60 rows for testing)
    train = df[:-30]
    test = df[-30:]

    # fit the VAR model
    model = VAR(train)
    results = model.fit()

    # create lagged values for the test data
    lags = results.k_ar
    test_data = test.values
    history = train.values[train.shape[0]-lags:]
    predictions = []

    # forecast for the test data
    for t in range(test_data.shape[0]):
        model_input = history[-lags:]
        yhat = results.forecast(model_input, steps=1)
        predictions.append(yhat[0])
        history = np.vstack([history, test_data[t]])

    # create a dataframe of predictions and actual values
    pred_df = pd.DataFrame(predictions, index=test.index, columns=df.columns)
    actual_df = test

    # get the predicted values as a list of dictionaries
    predicted_cf = pred_df[building].reset_index().to_dict('records')


    # return the predicted values
    return predicted_cf

def get_actual_cf(building):
    # load the data
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cf.csv"))
    df = pd.read_csv(file_path)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%Y")


    # Set 'Date' column as the index
    df.set_index('Date', inplace=True)
    df.index.freq = pd.infer_freq(df.index)

    # create a dataframe with only the required columns (KwH, max_temp, min_temp)
    df = df[[building, 'MaxTemperature', 'MinTemperature']]

    # split the data into train and test sets (use the last 60 rows for testing)
    test = df[-30:]

    # create a dataframe of predictions and actual values
    actual_df = test

    # get the predicted values as a list of dictionaries
    actual_cf = actual_df[building].reset_index().to_dict('records')


    # return the predicted values
    return actual_cf
