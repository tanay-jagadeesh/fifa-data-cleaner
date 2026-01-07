import pandas as pd

class FIFADataCleaner:

    def __init__(self):
        self.df = pd.read_csv('fifa-data-cleaner/fifa_raw_data.csv', low_memory = False)

        # Row Count
        self.count = len(self.df)

        #Empty dict.
        self.report = {}

        print(self.df.head())

    def clean_value_wage_clause(self):
        #Removing Pound Symbol
        for i in ['Value', 'Wage', 'Release Clause']:
            self.df[i] = self.df[i].str.replace('€', '')
        #Multiplying by ($)1000 if ends with K
        for i in ['Value', 'Wage', 'Release Clause']:
            self.df[i] = self.df[i].str.replace('K', '000')

