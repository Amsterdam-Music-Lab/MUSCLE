class CsvStringBuilder(object):
    def __init__(self):
        self.csv_string = []

    def write(self, row):
        self.csv_string.append(row)