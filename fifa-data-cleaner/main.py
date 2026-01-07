from data_cleaner import FIFADataCleaner
import os

# Get file size before cleaning
raw_file_size = os.path.getsize('fifa-data-cleaner/fifa_raw_data.csv') / (1024 * 1024) 
print(f"Raw file size: {raw_file_size:.2f} MB\n")

# Create instance and run cleaning
cleaner = FIFADataCleaner()

# Call clean() method
cleaner.clean()

# Call generate_report() method
cleaner.generate_report()

# Call save_clean_data() method
cleaner.save_clean_csv()

# Get file size after cleaning
clean_file_size = os.path.getsize('fifa-data-cleaner/fifa21_clean_data.csv') / (1024 * 1024)
print(f"\nClean file size: {clean_file_size:.2f} MB")
print(f"File size difference: {raw_file_size - clean_file_size:.2f} MB")