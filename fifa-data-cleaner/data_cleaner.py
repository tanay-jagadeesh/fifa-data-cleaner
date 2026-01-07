import pandas as pd

class FIFADataCleaner:

    def __init__(self):
        self.df = pd.read_csv('fifa_raw_data.csv', low_memory = False)

        # Row Count
        self.count = len(self.df)

        #Empty dict.
        self.report = {}
