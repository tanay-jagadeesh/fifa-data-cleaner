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

        self.report['value_wage_clause'] = self.df[['Value', 'Wage', 'Release Clause']].notna().count()

        print(self.report)

    def clean_height_weight(self):
        #Convert feet/inches to cm
        mask = self.df['Height'].str.contains("'")

        split_values = self.df.loc[mask, 'Height'].str.split("'", expand = True)

        feet_in_cm = split_values[0].astype(float) * 30.48
        inches_in_cm = split_values[1].astype(float) * 2.54
        total_cm = feet_in_cm + inches_in_cm

        self.df.loc[mask,'Height'] = total_cm

        #Convert lbs to kgs 

        mask_2 = self.df['Weight'].str.contains('lbs')

        total_kg = self.df.loc[mask_2, 'Weight'].str.replace('lbs', '').astype(float) * 0.453592

        self.df.loc[mask_2, 'Weight'] = total_kg

        #Replacing cm
        self.df['Height'] = self.df['Height'].str.replace('cm', '')

        #Replacing kg
        self.df['Weight'] = self.df['Weight'].str.replace('kg', '')

        #Converting to float
        self.df['Height'] = self.df['Height'].astype('float')
        self.df['Weight'] = self.df['Weight'].astype('float')

        self.report['height_weight_cleaned'] = self.df[['Height', 'Weight']].notna().count()

        print(self.report)

    def clean_contract_dates(self):
        #Made contract_start and contract_end

        split_contract = self.df['Contract'].str.split('~', expand = True)

        self.df['contract_start'] = pd.to_numeric(split_contract[0], errors = 'coerce')

        self.df['contract_end'] = pd.to_numeric(split_contract[1], errors = 'coerce')

        #Filled missing values
        self.df['contract_start'] = self.df['contract_start'].fillna('Free Agent')
        self.df['contract_end'] = self.df['contract_end'].fillna('Free Agent')

        #Count total pparsed
        total_start = self.df['contract_start'].notna().sum()
        total_end = self.df['contract_end'].notna().sum()

        total_parsed = total_start + total_end

        #Added result to dictionary
        self.report['contract_dates_parsed'] = total_parsed
        print(self.report)

    def handle_missing_values(self):
        
        missing_before = self.df.isnull().sum().sum()

        self.df['Loan Date End'] = self.df['Loan Date End'].fillna('Not on Loan')

        self.df['Hits'] = self.df['Hits'].fillna(0)

        self.df = self.df.fillna(0)

        missing_after = self.df.isnull().sum().sum()

        total_filled = missing_before - missing_after

        self.report['handle_missing_values'] = total_filled

        print(self.report)
        