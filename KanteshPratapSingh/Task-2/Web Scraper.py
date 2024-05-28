import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def fetch_html(url):
    """Fetch HTML content from a given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

def parse_html(html):
    """Parse HTML content and extract data."""
    soup = BeautifulSoup(html, 'html.parser')
    data = []

    # Extracting table data from Wikipedia
    table = soup.find('table', {'class': 'wikitable'})
    if table:
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            row_data = [col.text.strip() for col in cols]
            if row_data:
                data.append(row_data)
        return headers, data
    else:
        print("Table not found")
        return None, None

def save_to_csv(headers, data, filename):
    """Save data to a CSV file."""
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_to_json(headers, data, filename):
    """Save data to a JSON file."""
    data_dict = [dict(zip(headers, row)) for row in data]
    with open(filename, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(f"Data saved to {filename}")

def main():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    html = fetch_html(url)
    
    if html:
        headers, data = parse_html(html)
        
        if headers and data:
            csv_filename = 'countries_population.csv'
            json_filename = 'countries_population.json'
            
            save_to_csv(headers, data, csv_filename)
            save_to_json(headers, data, json_filename)
        else:
            print("No data found to save.")
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    main()
