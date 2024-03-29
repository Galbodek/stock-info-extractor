# Trading-Information-Script

**Overview**
This trading script is designed to extract and analyze stock information using the IEX Cloud API. It provides functionalities to fetch key statistics, financials, and other relevant data for the tickers available from IEX Cloud API. The script calculates a Net Net Score for each stock and identifies potentially undervalued stocks based on the Net Net Score and PE.


Sure, here's a README file for your GitHub repository:

Stock Information Extractor
This Python script extracts key financial information about stocks using the IEX Cloud API. It retrieves various metrics such as market cap, current assets, total liabilities, P/E ratio, and more. The script also calculates the Net Net Score and potential gain value based on the current stock price.

**Prerequisites**
-Python 3.x
-Required Python packages (install via pip):
  iexfinance
  pandas
  tqdm

**Usage**
1. Obtain an IEX Cloud token from IEX Cloud.
2. Run the script with the following command:
   python stock_info_extractor.py -iex-token YOUR_TOKEN -output OUTPUT_FILE_NAME -OBI-strict True/False

   Replace YOUR_TOKEN with your IEX Cloud token, OUTPUT_FILE_NAME with the desired output file name (optional), 
   and True/False with whether to use strict OBI criteria (cash_flow + (receivables * 0.75) + (inventory * 0.5), (optional, default is     False).

**Acknowledgments**
This script utilizes the library [iexfinance](https://github.com/addisonlynch/iexfinance?tab=readme-ov-file) for interacting with the [IEX Cloud API](https://iexcloud.io/) for financial data extraction.




  

