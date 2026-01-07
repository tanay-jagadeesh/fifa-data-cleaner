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
        for i in ['Value', 'Wage', 'Release Clause']:
            #Removing Pound Symbol
            self.df[i] = self.df[i].str.replace('€', '')

            #Replacing K with 000 ($1000)
            self.df[i] = self.df[i].str.replace('K', '000')

            #Replacing M with 000000 ($1000000)
            self.df[i] = self.df[i].str.replace('M', '000000')

            #Converting to float
            self.df[i] = self.df[i].astype('float')

        self.report = self.df[['Value', 'Wage', 'Release Clause']].notna().count()

        print(self.report)


