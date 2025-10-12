import requests
import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path
# Import database connection functions
from py_connection import *
from dotenv import load_dotenv
load_dotenv()

# Function to get stock data from EODHD API

def get_stock_data(stock_symbol, start_date = "", end_date = ""):
    # Replace {your-api-key} with your EODHD API key
    api_key = os.getenv('eodhd-api-key')
    generated_folder = os.getenv('generated-folder-path')

    stock_file = f'{generated_folder + stock_symbol}.json'

    # Date formatting
    date_format = "%Y-%m-%d"

    # Validate and parse input dates
    try:
        # If no start_date is provided, use today's date
        if len(start_date) == 0 :
            in_date = datetime.strftime(datetime.now(), date_format)
        else :
            in_date = datetime.strptime(start_date, date_format).date()
        
        # If no end_date is provided, use today's date
        if len(end_date) == 0 or len(end_date) < 10 :
            out_date = datetime.strftime(datetime.now(), date_format)
        else :
            out_date = datetime.strptime(end_date, date_format).date()

    except Exception as e:
        # Handle invalid date formats
        print("Date parameter should be in the following format : yyyy-MM-dd e.g. 2025-01-31" )

    finally:
        # Notify user that the task is complete
        print("Task complete")

    # Construct the API URL
    url = f"https://eodhd.com/api/eod/{stock_symbol}.PSE?from={in_date}&to={out_date}&period=d&api_token={api_key}&fmt=json"

    # For debugging purposes, you can uncomment the next line to see the constructed URL.
    # print(url)

    # Check if the stock file already exists
    if os.path.exists(stock_file):
        
        # If it exists, remove it and fetch fresh data
        os.remove(stock_file)

        # Fetch data from the API
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

        # Save the fetched data to a JSON file
        with open(stock_file, 'w') as f:
            json.dump(data, f, indent=4)

        # Notify user of successful operation
        return {'status': 'success', 'file': stock_file}

    else:
        # If the file does not exist, fetch data from the API
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Save the fetched data to a JSON file
            with open(stock_file, 'w') as f:
                json.dump(data, f, indent=4)

            # Notify user of successful operation
            return {'status': 'success', 'file': stock_file}

def check_and_create_directories():
    generated_files_folder = os.getenv('generated-folder-path')
    processed_files_folder = os.getenv('processed-folder-path')

    if not os.path.exists(generated_files_folder):
        os.makedirs(generated_files_folder)
        print(f"Created directory: {generated_files_folder}")

    if not os.path.exists(processed_files_folder):
        os.makedirs(processed_files_folder)
        print(f"Created directory: {processed_files_folder}")

def check_files_in_directory(directory, extension=".json"):

    files = [f for f in os.listdir(directory) if f.endswith(extension)]
    return files

if __name__ == "__main__":

    # Check if necessary directories exist, if not create them
    check_and_create_directories()
    # Get the folder path from environment variable
    generated_files_folder = os.getenv('generated-folder-path')

    # stock_codes = input("Enter multiple PSE stock codes separated by commas (e.g., 'AP,JFC,ALI'): ")
    has_stock_files = input("Do you have existing stock data files to load into the database? (Y/N) ").lower()

    # Validate user input
    if has_stock_files not in ['y', 'n']:
        print("Invalid input. Please enter 'Y' or 'N'.")
        exit()

    # If user has existing stock files, process them
    if has_stock_files == 'y':

        # List all JSON files in the generated files directory
        json_files = [f for f in os.listdir(generated_files_folder) if f.endswith('.json')]

        # For debugging purposes, you can uncomment the next line to see the list of JSON files found.
        # print(json_files)
        
        # If no JSON files are found, notify the user
        if not json_files:
            print("No JSON files found in the specified directory.")

        else:
            # Process each JSON file and load data into the database
            for json_file in json_files:
                # Check if the file exists before processing
                if os.path.exists(generated_files_folder + json_file):

                    # Notification of the file being processed
                    print(f"Processing file: {json_file}")

                    # Load data into the database
                    dump_stock_data_to_db(generated_files_folder + json_file, connect_to_db())

            print("All files processed.")
    else:

        stock_codes = input("Enter multiple PSE stock codes separated by commas (e.g., 'AP, JFC, ALI'): ") or "---"
        stock_date_start = input("Enter start date (yyyy-MM-dd) or press Enter for today: ") or datetime.now().strftime("%Y-%m-%d")
        stock_date_end = input("Enter end date (yyyy-MM-dd) or press Enter for today: ") or datetime.now().strftime("%Y-%m-%d")

        if stock_codes not in ["", "---"]:
            # Check if stock_codes is a single code or multiple codes
            if ',' not in stock_codes:
                stock_codes = [stock_codes.strip().upper()]
            else:   
                stock_codes = stock_codes.upper().split(',')

            # Just to make sure that the stock codes are stripped of any leading/trailing spaces
            stock_codes = [code.strip() for code in stock_codes]

            # For debugging purposes, you can uncomment the next line to see the list of stock codes.
            # print(stock_codes)

            # List to hold generated stock files
            stock_files = []
            
            # Process each stock code    
            for sc in stock_codes:

                # Automatically remove existing stock file if exists
                if os.path.exists(f"{sc}.json"):
                        os.remove(f"{sc}.json")

                # Generate stock data file for each stock code
                stock_file_generated = get_stock_data(stock_symbol=sc, start_date=stock_date_start, end_date=stock_date_end)
                if  stock_file_generated['status'] == 'success':
                    
                    # Store the generated stock files in a list
                    stock_files.append(stock_file_generated['file'])

                    # Initialize database connection and dump stock data to database
                    print(f"Loading stock {sc} data to database...")
                    dump_stock_data_to_db(stock_file_generated['file'], connect_to_db())

                    # Notify user of completion for each stock code
                    print(f"Completed processing for {stock_file_generated['file']}.")
                    
                else:
                    # Notify user if no stock data file was generated for the stock code
                    print(f"No stock data file to process for {sc}.")

            # Final notification after all stock codes are processed
            print("All stock codes processed.")
        else:
            # Notify user if no stock codes were provided
            print("No stock codes provided. Exiting.")