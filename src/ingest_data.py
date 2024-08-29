import requests

def fetch_data(base_url):
    current_page = 1
    total_pages = 1
    complete_data = []

    while current_page <= total_pages:
        page_url = f"{base_url}?page={current_page}"
        response = requests.get(page_url)

        if response.status_code == 200:
            response_data = response.json()
            page_data = response_data.get('body', {}).get('data', [])
            total_pages = response_data.get('body', {}).get('total_pages', 0)
            complete_data.extend(page_data)
            print(f"Processing Page {current_page}...")
            current_page += 1
        else:
            print(f"Failed to retrieve data from page {current_page}: {response.status_code}")
            break

    return complete_data