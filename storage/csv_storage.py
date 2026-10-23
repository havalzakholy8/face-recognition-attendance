# storage/csv_storage.py
import csv
import os
from exceptions import StorageError

class CSVStorage:
    """Handles reading and writing CSV files"""
    
    @staticmethod
    def save_to_csv(filename, data, fieldnames):
        """Saves data to a CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Successfully saved data to {filename}")
        except Exception as error:
            raise StorageError(f"Could not save to {filename}: {error}")
    
    @staticmethod
    def load_from_csv(filename):
        """Loads data from a CSV file"""
        # If file doesn't exist, return empty list
        if not os.path.exists(filename):
            return []
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
            print(f"Successfully loaded data from {filename}")
            return data
        except Exception as error:
            raise StorageError(f"Could not load from {filename}: {error}")
