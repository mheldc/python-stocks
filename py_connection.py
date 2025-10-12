import pyodbc
import os
import shutil 
import json
from dotenv import load_dotenv
load_dotenv()

def connect_to_db():
    db_server = os.getenv('db-host-name')
    db_name = os.getenv('db-name')
    db_trust = os.getenv('trust-server-certificate')
    db_driver = os.getenv('db-driver')
    try:
        cn = pyodbc.connect(
            'DRIVER='+ db_driver +';'
            'SERVER='+ db_server +';'
            'DATABASE=' + db_name + ';'
            'Trusted_Connection=' + db_trust +';'
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
    else:
        print("Database connection successful")
        return cn

def close_db_connection(cn):
    if cn:
        cn.close()
        print("Database connection closed.")

def dump_stock_data_to_db(JSON_file, cn):
    processed_folder = os.getenv('processed-folder-path')
    generated_folder = os.getenv('generated-folder-path')

    # For debugging purposes, you can uncomment the next line to see the JSON file being processed.
    print(JSON_file)

    # Check if the database connection is valid
    if not cn:
        print("No valid database connection.")
        return

    # Check if the specified JSON file exists
    if os.path.exists(JSON_file):

        # Open and load the JSON data from the file
        with open(JSON_file, 'r') as json_data:
            data = json.load(json_data)

            # For debugging purposes, you can uncomment the next line to see the loaded data.
            # print(data)

            # User notification that the process is starting.
            print(f"Loading stock data {JSON_file.replace('.json', '')} to database...")

            # Iterate through each record in the JSON data and insert into the database.
            for jd in range(len(data)):
                stock_symbol = JSON_file.replace('.json', '').replace(generated_folder, '')
                stock_date = data[jd]['date']
                open_price = data[jd]['open']
                high_price = data[jd]['high']
                low_price = data[jd]['low']
                close_price = data[jd]['close']
                adj_close_price = data[jd]['adjusted_close']  
                volume = data[jd]['volume']

                # Using a stored procedure to upsert data
                query = f"Exec sp_upsert_stock_data  @stock_code = '{stock_symbol}', @stock_date = '{stock_date}', @stock_open = {open_price}, @stock_close = {close_price}, @stock_high = {high_price}, @stock_low = {low_price}, @stock_adj_close = {adj_close_price}, @stock_volume = {volume}"
                
                # For debugging purposes, you can uncomment the next line to see the generated query.
                # print(query)

                # Execute the query and commit the transaction.
                cursor = cn.cursor()
                cursor.execute(query)
                cn.commit()
        
        # Notify user of completion and number of records inserted.
        print(f"Inserted {len(data)} record/s for stock code {stock_symbol}.")

        # Move processed file to the processed-files folder
        generated_file = JSON_file
        processed_file = JSON_file.replace(generated_folder, processed_folder)

        # For debugging purposes, you can uncomment the next line to see the file move operation.
        print(f"Generated File: {generated_file} \n Processed File: {processed_file}")

        # Move the file and handle any exceptions
        try:
            shutil.move(generated_file, processed_file)
        except Exception as e:
            print(f"Error moving file {JSON_file} to processed-files folder: {e}")    

    else:
        # Notify user if the specified JSON file does not exist.
        print(f"File {JSON_file} does not exist.")