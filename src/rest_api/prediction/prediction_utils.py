from collections import defaultdict
import numpy as np
import csv
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os


def get_prediction(stock_name=None):
    data_for_prediction = defaultdict(dict)
    get_data_set(data_for_prediction)
    if not stock_name:
        return
    prediction = calculate_prediction(data_for_prediction[stock_name])
    return prediction


def calculate_prediction(data):
    x_data = np.asarray(data['x_axis'], dtype=np.float32)
    x_train, x_test, y_train, y_test = train_test_split(x_data, data['close'], test_size=0.9, random_state=0)
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)
    prediction = regressor.predict(x_test)
    return prediction


def get_data_set(data_for_prediction):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_dir, 'dow_jones_index_data')
    if not os.path.isfile(file_path):
        raise Exception('File not found')
    with open(file_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, quotechar=',')
        skip_first_row = True
        for row in csv_reader:
            if skip_first_row:
                skip_first_row = False
                continue
            if not data_for_prediction[row[1]]:
                data_for_prediction[row[1]]['x_axis'] = []
                data_for_prediction[row[1]]['close'] = []
            data_for_prediction[row[1]]['x_axis'].append([row[4][1:], row[5][1:], row[3][1:], row[7][1:]])
            data_for_prediction[row[1]]['close'].append(row[6][1:])
