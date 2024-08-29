import os
from src.ingest_data import fetch_data
from src.store_file import store_data
from src.calculate import calculate_revenue_churn
from dotenv import load_dotenv
load_dotenv()


def main():
    os.environ['BASE_URL'] = os.getenv('BASE_URL')
    os.environ['CSV_FILENAME'] = os.getenv('CSV_FILENAME')

    # fetch records
    if os.environ['BASE_URL']:
        data = fetch_data(os.environ['BASE_URL'])
        print(f"Retrieved {len(data)} records.")
    else:
        print("BASE_URL environment variable is not set.")

    # TASK 1
    store_data(data, os.environ['CSV_FILENAME'])
    print('TASK 1: File Downloaded!')

    # TASK 2
    calculate_revenue_churn(os.environ['CSV_FILENAME'])
    print('TASK 2: Desired Table Generated!')


if __name__ == "__main__":
    main()