# stock-info-extractor

## Overview
This script is designed to extract and analyze stock information using the IEX Cloud API. It provides functionalities to fetch key statistics, financials, and other relevant data for the tickers available from IEX Cloud API. The script calculates a Net Net Score for each stock and identifies potentially undervalued stocks based on the Net Net Score and PE.

## Prerequisites
-Python 3.x <br />
-Required Python packages (install via pip): <br />
> iexfinance <br />
> pandas <br />
> tqdm <br />

## Usage
1. Obtain an IEX Cloud token from IEX Cloud.
2. Run the script with the following command: <br /><br />
   ```bash
   python extract_stock_info.py -iex-token YOUR_TOKEN -output OUTPUT_FILE_NAME -OBI-strict 0/1
<br />
 Replace YOUR_TOKEN with your IEX Cloud token, OUTPUT_FILE_NAME with the desired output file name (optional), 
 and 0/1 with whether to use strict OBI criteria (cash_flow + (receivables * 0.75) + (inventory * 0.5), (optional, default is     False).<br /><br />

3. After running the script, the output will be saved to an Excel file named OUTPUT_FILE_NAME_<current_date>.xlsx. This file will contain comprehensive information about the stocks retrieved.


## Acknowledgments
This script utilizes the library [iexfinance](https://github.com/addisonlynch/iexfinance?tab=readme-ov-file) for interacting with the [IEX Cloud API](https://iexcloud.io/) for financial data extraction.




  

