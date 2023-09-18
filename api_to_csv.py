"""
api_to_csv.py

Author: Erik Hanson
Date: 2023-09-16
Version: 1.0

Description:
This Python script fetches data from Shopify using GraphQL API calls.
The queried data is then parsed and saved into a CSV file, which allows for easy analysis
of specific groupings of data within Shopify API. The script is designed to handle API pagination
and common error scenarios. 

The default query in this script fetches all product variants from the specified Shopify store
along with some of their most important data. My intention with this script is that it is useful for
any GraphQL API query. One would simply replace the default GRAPHQL_QUERY variable with their own
and then modify the JSON parsing block of code below to match the contents of the query. 

This script was developed because, as I learned more about utilizing Shopify's data to improve 
aspects of my business' operations, I found myself constantly needing to manually join product, 
inventory, and sales data exports in order to get the information I wanted together into one
table.

This script assumes that you have created a custom app within a Shopify and have been granted an 
API key from it.


Dependencies:
- Python 3.x
- 'requests' Python package
- 'csv' Python package
- 'time' Python package

Environment Setup:
- Requires a separate 'credentials.py' file for storing API keys and passwords.
- Ensure this 'credentials.py' is listed in the '.gitignore' file.

Usage:
python api_to_csv.py

Output:
CSV file saved in the '/csv/' directory, named 'products.csv'.

"""

import requests
import csv
import time

from credentials import SHOPIFYAPI_KEY, SHOPIFYPW, SHOPIFYSITE 


API_VERSION = '2023-01'

## The GraphQL query string goes here. Note that this script is set up
## to handle paginiation. Shopify has a GraphQL explorer app that is
## geat for finding and testing queries. Once you have your query,
## you'll need to scroll down and edit the 'Parse the JSON' block and specify
## which queried data gets written under which csv file headers. 

GRAPHQL_QUERY = """
query ($cursor: String) {
  productVariants(first: 25, after: $cursor) {
    pageInfo {
      hasNextPage
    }
    edges {
      cursor
      node {
        sku
        inventoryItem {
          id
        }
        product {
          title
          productType
          vendor
          createdAt
          updatedAt
        }
        title
        price
        barcode
      }
    }
  }
}
"""

## Connect to Shopify's GraphQL API
## Note that all GraphQL requests, queries and mutations both, 
## are handled through the POST method.

def fetch_query():
    """
    Connects to Shopify's GraphQL API and fetches product variant data.
    Handles pagination and the following errors:
    - API Throttling: Waits for 10 seconds before retrying.
    - Other GraphQL errors: Prints the error and breaks the loop.
    
    Returns:
        List of dictionaries containing the queried data fields.
    """
    shop_url = f"https://{SHOPIFYAPI_KEY}:{SHOPIFYPW}@{SHOPIFYSITE}/admin/api/{API_VERSION}/graphql.json"
    query = []

    has_next_page = True
    variables = {}

    while has_next_page:
        response = requests.post(shop_url, json={'query': GRAPHQL_QUERY, 'variables': variables})
        json_data = response.json()

        if 'errors' in json_data:
            error_code = json_data['errors'][0].get('extensions', {}).get('code', '')

            if error_code == 'THROTTLED':
                print("Throttled. Waiting for 10 seconds before retrying...")
                time.sleep(10)
                continue
            else:
                print("Error(s) encountered:", json_data['errors'])
                break

        if 'data' not in json_data:
            print("Unexpected response:", json_data)
            break
        
## Parse the JSON. This block is particular to the specific GraphQL query
## defined above in the 'GRAPHQL_QUERY' variable. The query.append() function
## contains the csv file headers and the json data that will get written under
## those headers. This block needs to get written or adjusted according to the
## particular GraphQL query you want to run. 

        query_data = json_data['data']['productVariants']

        for edge in query_data['edges']:
            variant = edge['node']
            inventory_item_id_url = variant['inventoryItem']['id'] # This 'inventory_item_id' prep is for my own particular use case.
            inventory_item_id = inventory_item_id_url.split('/')[-1]  # This splits the URL by '/' and gets the last part
            query.append({
                'sku': variant['sku'],
                'inventory_item_id': inventory_item_id,
                'price': variant['price'],
                'variant_title': variant['title'],
                'product_type': variant['product']['productType'],
                'vendor': variant['product']['vendor'],
                'created_at': variant['product']['createdAt'],
                'updated_at': variant['product']['updatedAt'],
                'barcode': variant['barcode'],
                'product_title': variant['product']['title']
            })

        has_next_page = query_data['pageInfo']['hasNextPage']
        if has_next_page:
            last_cursor = query_data['edges'][-1]['cursor']
            variables = {"cursor": last_cursor}

    return query

def save_to_csv(data, filename):
    """
    Saves the provided data into a CSV file with a specified filename.
    
    Parameters:
        - data: List of dictionaries containing the queried data fields.
        - filename: The name of the CSV file to save the data in.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    """
    Main function to execute the query fetching and CSV writing process.
    """
    query = fetch_query()
    save_to_csv(query, './csv/products.csv')

if __name__ == "__main__":
    main()