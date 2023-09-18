This script demonstrates fetching product variant data from
Shopify via GraphQL API. The query is returned as a JSON object
and then parsed and written into a CSV file. 

This script was developed because as I learned more about utilizing 
Shopify's data to improve our operations, I found myself constantly 
needing to manually join product, inventory, and sales data 
exports in order to get the information I wanted together in one
table. Once I realized what GraphQL API could do, now I query the specific 
data I want to perform analysis on, and it's all ready in one table.

This script assumes that you have a Shopify account, and have 
first created a custom app there, in order to get an API key.

1. Set up a 'credentials.py' file with your API key, Shopify site, and password. If you are publishing your own version of this script anywhere public make sure that your passwords are kept secret by using the .gitignore file.

2. Use the Shopify GraphQL app, or the GraphQL explorer webapp to generate your query.

3. Define your csv's column headers and assign the corresponding query data in the code block that parses the JSON.
 
4. CSV files are saved to /csv. 

Future development of this project would include being able to run the script from the command line with a query/parsing instructions file as an argument. Having separate, pre-set query/parse configuration files for the queries that I run the most, so that they can be simply referenced as an argument, without needing to manually edit the parsing block would be pretty sweet. 
