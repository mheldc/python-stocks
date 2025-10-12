# Stocks Python Exercises

This repository contains Python exercises and scripts related to stock data analysis and processing.

## Features

- Stock price extraction for EODHD API
- Connecting to a database and inserting data using stored procedures
- Loading environment variables from `.env` files for configuration
- Processing and loading stock data from JSON files
- Moving processed files to a designated folder after database insertion
- Data visualization (Power BI)

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/mheldc/python-stocks.git
    ```
2. Navigate to the `python-stocks` directory:
    ```bash
    cd python-stocks
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create your .env variables.

5. Add .env to your .gitignore file

6. Must have an account to EODHD in order to use the API call on the code.
    https://eodhd.com/
   If you have subscribed or access to other stock market API's, you just need to replace the API url: (On py_stocks.py line 47)

7. SQL script file is included in this repository. If you want to use other database environments, you may do so.
   Simply change the connection string on py_connection.py lines 15 - 18

## Usage

Run any of the example scripts:
```bash
python py_stocks.py
```

## Main Functions

### py_connection.py

- **connect_to_db()**  
  Establishes a connection to the database using environment variables for configuration.  
  **Usage:**  
  ```python
  from py_connection import connect_to_db
  cn = connect_to_db()
  ```

- **close_db_connection(cn)**  
  Closes the provided database connection.  
  **Usage:**  
  ```python
  from py_connection import close_db_connection
  close_db_connection(cn)
  ```

- **dump_stock_data_to_db(JSON_file, cn)**  
  Loads stock data from a JSON file and inserts it into the database using a stored procedure. Moves the processed file to a designated folder.  
  **Usage:**  
  ```python
  from py_connection import dump_stock_data_to_db
  dump_stock_data_to_db('path/to/stock.json', cn)
  ```

### py_stocks.py

- **Main script for orchestrating stock data extraction, processing, and database insertion.**  
  Typical usage involves:
  1. Connecting to the database.
  2. Processing or generating stock data files.
  3. Calling `dump_stock_data_to_db` for each file.
  4. Closing the database connection.

  **Example:**
  ```python
  from py_connection import connect_to_db, dump_stock_data_to_db, close_db_connection

  cn = connect_to_db()
  dump_stock_data_to_db('generated-files/ABC.json', cn)
  close_db_connection(cn)
  ```

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.