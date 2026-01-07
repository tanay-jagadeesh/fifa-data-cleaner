import pandas as pd
import numpy as np
import time

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
        #Missing Before
        missing_before = self.df.isnull().sum().sum()

        #Filling Data
        self.df['Loan Date End'] = self.df['Loan Date End'].fillna('Not on Loan')

        self.df['Hits'] = self.df['Hits'].fillna(0)

        self.df = self.df.fillna(0)

        #Missing After
        missing_after = self.df.isnull().sum().sum()

        total_filled = missing_before - missing_after

        #Assigning the missing values filed to total_filled
        self.report['handle_missing_values'] = total_filled

        print(self.report)

    def fix_column_names(self):
        # Convert to lowercase
        self.df.columns = self.df.columns.str.lower()

        # Replace spaces with underscores
        self.df.columns = self.df.columns.str.replace(' ', '_')

        # Remove special characters 
        self.df.columns = self.df.columns.str.replace('[^a-z0-9_]', '', regex=True)

        total_columns = len(self.df.columns)

        self.report['columns_renamed'] = total_columns

        print(self.report)

    def fix_star_ratings(self):
        #Replace Star Ratings/Convert to int
        self.df['W/F'] = self.df['W/F'].str.replace('★', '')

        self.df['W/F'] = self.df['W/F'].astype('int')

        self.df['SM'] = self.df['SM'].str.replace('★', '')

        self.df['SM'] = self.df['SM'].astype('int')

        #Count total converted
        total_wf = self.df['W/F'].notna().sum()

        total_sm = self.df['SM'].notna().sum()

        total_ratings = total_wf + total_sm

        #Assign it to total_ratings
        self.report['star_ratings'] = total_ratings

        print(self.report) 

    def remove_url_columns(self):
        total_before = len(self.df.columns)

        self.df = self.df.drop(columns = ['photoUrl', 'playerUrl'])

        total_after = len(self.df.columns)

        total = total_before - total_after

        self.report['columns_dropped'] = total

        print(self.report)

    def fix_data_types(self):
        # Make sure Age is int
        self.df['Age'] = self.df['Age'].astype('int')

        # Make sure all stat columns (Crossing, Finishing, etc.) are int
        total_stats = 0
        for i in ['Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys',
                  'Dribbling', 'Curve', 'FKAccuracy', 'LongPassing', 'BallControl',
                  'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                  'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots',
                  'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties',
                  'Composure', 'Marking', 'StandingTackle', 'SlidingTackle',
                  'GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes']:
            self.df[i] = self.df[i].astype('int')
            self.df[i] = pd.to_numeric(self.df[i], errors = 'coerce')
            total_stats += self.df[i].notna().sum()

        total_value_wage = 0
        for i in ['Value', 'Wage']:
            self.df[i] = self.df[i].astype('float')
            total_value_wage += self.df[i].notna().sum()

        # Count total values converted
        total_age = self.df['Age'].notna().sum()
        total_converted = total_age + total_stats + total_value_wage

        self.report['fix_data_types'] = total_converted

        print(self.report)

    def create_derived_features(self):
        #Contract length calculation
        self.df['contract_length'] = self.df['end_year'] - self.df['start_year']

        #Value per column calculation
        self.df['value_per_column'] = self.df['value'] / self.df['ova']

        #Conditional based on age using np.where
        self.df['age_group'] = np.where(self.df['age'] < 25, 'Young',
                        np.where(self.df['age'] < 30, 'Prime', 'Veteran'))

        #Count
        new_features = 3

        self.report['derived_features'] = new_features
        print(self.report)

    def clean(self):

        # Print header
        print("Starting FIFA Data Cleaning Process")

        # Track start time
        start_time = time.time()

        # Call all cleaning methods in order
        self.clean_value_wage_clause()
        self.clean_height_weight()
        self.clean_contract_dates()
        self.handle_missing_values()
        self.fix_column_names()
        self.fix_star_ratings()
        self.remove_url_columns()
        self.fix_data_types()
        self.create_derived_features()

        # Track end time
        end_time = time.time()
        total_time = end_time - start_time

        # Print footer
        print(f"Data Cleaning Complete!")
        print(f"Total time: {total_time:.2f} seconds")
        print("\nFinal Report:")
        print(self.report)
    
    def generate_report(self):
        print("FIFA DATA CLEANING REPORT")

        # Original rows vs final rows
        final_rows = len(self.df)
        print(f"\nOriginal rows: {self.count}")
        print(f"Final rows: {final_rows}")

        # Columns before vs after
        final_columns = len(self.df.columns)
        print(f"\nFinal columns: {final_columns}")

        # Currency conversions done
        print(f"\nCurrency conversions done: {self.report.get('value_wage_clause', 'N/A')}")

        # Height/weight conversions done
        print(f"Height/weight conversions done: {self.report.get('height_weight_cleaned', 'N/A')}")

        # Contract dates parsed
        print(f"Contract dates parsed: {self.report.get('contract_dates_parsed', 'N/A')}")

        # Missing values filled
        print(f"Missing values filled: {self.report.get('handle_missing_values', 'N/A')}")

        # Column names fixed
        print(f"Column names fixed: {self.report.get('columns_renamed', 'N/A')}")

        # Data quality score
        total_cells = self.df.shape[0] * self.df.shape[1]
        non_null_cells = self.df.notna().sum().sum()
        quality_score = (non_null_cells / total_cells) * 100

        print(f"\nData quality score: {quality_score:.2f}%")