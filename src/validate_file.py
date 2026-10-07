import csv

def is_valid_file(filename, required_columns):

    with open(filename,"r")as file: 
        header = csv.reader(file)
        column_names = next(header)

        return len(column_names) == len(required_columns) and  tuple(column_names) == required_columns
