# api_to_csv.py

__Author: Erik Hanson__
__Date: 2023-09-16__
__Version: 1.0__

## Description:
This Python script fetches data from Shopify using GraphQL API calls.
The queried data is then parsed and saved into a CSV file, which allows for easy analysis
of specific groupings of data within Shopify API. The script is designed to handle API pagination and common error scenarios. 

The default query in this script fetches all product variants from the specified Shopify store along with some of their most important data. My intention with this script is that it is useful for any GraphQL API query. One would simply replace the default GRAPHQL_QUERY variable with their own and then modify the JSON parsing block of code below to match the contents of the query. 

This script was developed because, as I learned more about utilizing Shopify's data to improve aspects of my business' operations, I found myself constantly needing to manually join product, inventory, and sales data exports in order to get the information I wanted together into one table.

This script assumes that you have created a custom app within a Shopify and have been granted an API key from it.


## Dependencies:
- Python 3.x
- 'requests' Python package
- 'csv' Python package
- 'time' Python package

## Environment Setup:
- Requires a separate 'credentials.py' file for storing API keys and passwords.
- Ensure this 'credentials.py' is listed in the '.gitignore' file.

## Usage:
python api_to_csv.py

## Output:
CSV file saved in the '/csv/' directory, named 'products.csv'.

## Further Commentary:
This script was developed because, as I learned more about utilizing Shopify's data to improve my business' operations, I found myself constantly needing to manually join product, inventory, and sales data exports in order to get the information I wanted together into one table. Once I realized what Shopify's GraphQL API was capable of, I was happy to be able to query the specific data I wanted to perform analysis on and have it neatly together in one table.

Use the Shopify GraphQL app, or the GraphQL explorer webapp to generate queries.

Define your csv's column headers and assign the corresponding query data in the code block that parses the JSON.

## Future development: 

* Run the script from the command line with a query/parsing instructions file as an argument. Having separate, pre-set query/parse configuration files for the queries that I run the most, so that they can be simply referenced as an argument, without needing to manually edit the parsing block would be pretty sweet. 

* Refactor fetch_query function into separate functions that adhere to the Single Responsibility Principle.


