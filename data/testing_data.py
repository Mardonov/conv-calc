import csv
import os

file_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep


# Получить варианты входных данных и ожид. результатов из файла CSV
def read_csv_data(file):
    params_list = []
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            params_list.append(row)
    return params_list


def get_converter_data():
    return read_csv_data(file_dir + 'converter.csv')


def get_currencies_data():
    return read_csv_data(file_dir + 'currencies.csv')
