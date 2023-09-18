## This script demonstrates fetching product variant data from
## Shopify via GraphQL API. The query is returned as a JSON object
## and then parsed and written into a CSV file. 
##
## This script was developed because as I learned more about utilizing 
## Shopify's data to improve our operations, I found myself constantly 
## needing to manually join product, inventory, and sales data 
## exports in order to get the information I wanted together in one
## table. Now, I can query the specific data I want, and perform analysis
## on the csv that this script generates. 
##
## This script assumes that you have a Shopify account and have 
## first created a custom app there in order to get an API key.
##  
## CSV files are saved to /csv. 

import requests
import csv
import time

## IMPORTANT: Put your own secrets in a separate file called 'credentials.py'
## and make sure that it listend in your '.gitignore' file so that
## you don't accidentally share them. A truly better practice would be to
## work here with something like HashiCorp Vault, however I'm keeping this simple
## for the sake of demonstration.

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
    shop_url = f"https://{SHOPIFYAPI_KEY}:{SHOPIFYPW}@{SHOPIFYSITE}/admin/api/{API_VERSION}/graphql.json"
    query = []

    has_next_page = True
    variables = {}

    while has_next_page:
        response = requests.post(shop_url, json={'query': GRAPHQL_QUERY, 'variables': variables})
        json_data = response.json()

## Handle common errors

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

## API pagination handling

        has_next_page = query_data['pageInfo']['hasNextPage']
        if has_next_page:
            last_cursor = query_data['edges'][-1]['cursor']
            variables = {"cursor": last_cursor}

    return query

## Save the results of 

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    query = fetch_query()
    save_to_csv(query, '/csv/fula_products.csv')

if __name__ == "__main__":
    main()