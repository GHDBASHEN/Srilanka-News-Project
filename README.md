# Sri Lankan News Data Warehouse Project

This project is an end-to-end ETL pipeline that scrapes news articles from Sri Lankan news portals, processes the data, and loads it into a star schema data warehouse hosted on Azure MySQL.

## Project Structure

-   `/database`: Contains all SQL scripts to build the data warehouse schema.
-   `/python_etl`: Contains the main Python ETL script for scraping and loading data.
-   `requirements.txt`: A list of all necessary Python libraries.
-   `README.md`: This instruction file.

## How to Set Up and Run

### 1. Build the Database

-   Make sure your Azure MySQL Flexible Server is running.
-   Using a command line or a SQL client (like MySQL Workbench), connect to your database.
-   Run the SQL scripts located in the `/database` folder in the following order:
    1.  `schema/01_create_dimensions.sql`
    2.  `schema/02_create_facts.sql`
    3.  `seeds/01_seed_initial_data.sql`
    4.  `views/01_create_analytics_views.sql`

### 2. Set Up the Python Environment

-   It's recommended to use a Python virtual environment.
-   Install all required libraries by running the following command in your terminal:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configure the ETL Script

-   Open the `python_etl/scraper.py` file.
-   Update the `DB_CONFIG` dictionary with your actual Azure MySQL credentials (host, user, password, database).
-   Make sure you have downloaded the Azure SSL certificate (`DigiCertGlobalRootCA.crt.pem`) and placed it in the `python_etl/` directory.

### 4. Run the Pipeline

-   Navigate to the `python_etl/` directory in your terminal.
-   Execute the script:
    ```bash
    python scraper.py
    ```

The script will now scrape the latest articles, process them, and load them into your data warehouse. You can schedule this script to run periodically to keep your data fresh.