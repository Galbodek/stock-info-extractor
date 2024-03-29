from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols
import pandas as pd
import argparse
import datetime
from tqdm import tqdm
import random


def get_tickers(random_order: bool = False):
    """
    Get tickers of all companies
    :param random_order: whether to shuffle the tickers
    (in case a connection error occurs in the middle of the process)
    :return: list of tickers
    """
    lst = get_symbols(token=MY_TOKEN).symbol.tolist()
    if random_order:
        random.shuffle(lst)
    return lst


def get_stats(stock: Stock):
    """
    Get key stats of the stock
    :param stock: Stock object
    :return: dict of key stats
    """
    key_stats = stock.get_key_stats()
    if key_stats.shape[0] == 0:
        return None
    return key_stats.iloc[0].to_dict()


def get_financials(stock: Stock):
    """
    Get financials of the stock
    :param stock: Stock object
    :return: financials dict
    """
    fin = stock.get_financials()
    if fin.shape[0] == 0:
        return None
    else:
        return fin.iloc[0].to_dict()


def get_company_info(stock: Stock):
    """
    Get company information
    :param stock: Stock object
    :return: company information dict
    """
    company = stock.get_company()
    if company.shape[0] == 0:
        return None
    return company.iloc[0].to_dict()


def get_price(stock: Stock):
    """
    Get price of the stock
    :param stock: Stock object
    :return: price dict
    """
    price = stock.get_price()
    if 'price' not in price.index:
        return None
    return price.loc['price'][0]


def is_obi(x: pd.Series):
    """
    Check if the company is OBI (Net_net Score < 0.7 & PE < 100)
    :param x: Series
    :return: True if OBI, otherwise False
    """
    if x['PE'] is None or x['Net Net Score'] is None:
        return None

    return 0 < x['Net Net Score'] < 0.7 and 0 < x['PE'] < 100


def get_current_assets(stock: Stock, financials: dict, obi_strict: bool = False):
    """
    Get current assets of the stock
    :param financials: Financials dict
    :param stock: Stock object
    :param obi_strict: Whether calculate current assets strictly
    (cash_flow + (receivables * 0.75) + (inventory * 0.5))
    :return:
    """
    if obi_strict:
        cash_flow = stock.get_cash_flow()
        if cash_flow.shape[0] == 0:
            cash_flow = None
        else:
            cash_flow = cash_flow.iloc[0].to_dict().get('cashFlow', None)
        receivables = financials.get('receivables', None)
        inventory = financials.get('inventory', None)

        if None in (receivables, inventory, cash_flow):
            return financials.get('currentAssets', None)

        return cash_flow + (receivables * 0.75) + (inventory * 0.5)

    else:
        return financials.get('currentAssets', None)


def get_stock_info(ticker: str, obi_strict: bool = False):
    """
    Get stock information
    :param ticker: stock ticker
    :return: dict of stock information
    """
    stock = Stock(ticker, token=MY_TOKEN)

    stats = get_stats(stock)
    financials = get_financials(stock)
    if financials is None:
        return None
    company_info = get_company_info(stock)

    market_cap = stats.get('marketcap', None)

    current_assets = get_current_assets(stock, financials, obi_strict)
    total_liabilities = financials.get('totalLiabilities', None)

    if current_assets is None or total_liabilities is None or market_cap is None:
        return None

    net_net_score = market_cap / (current_assets - total_liabilities)

    current_stock_price = get_price(stock)
    destination_stock_price = current_stock_price * (1 / net_net_score) \
        if net_net_score != 0 else None
    gain_value = (destination_stock_price / current_stock_price) * 100 \
        if destination_stock_price is not None else None

    return {
        'Ticker': stock.symbols[0],
        'Company Name': company_info['companyName'],
        'Stock Market': company_info['exchange'],
        'Country': company_info['country'],
        'Sector': company_info['sector'],
        'Market Cap': market_cap,
        'Current Assets': current_assets,
        'Total Liabilities': total_liabilities,
        'Net Net Score': net_net_score,
        'PE': stats['peRatio'],
        'Current Stock Price': current_stock_price,
        'Destination Stock Price': destination_stock_price,
        'Gain Value': gain_value
    }


def get_stocks_info(tickers: list[str], obi_strict: bool = False):
    """
    Get stocks information
    :param tickers: list of tickers
    :return: stocks information dataframe
    """
    stocks_info = []
    progress_bar = tqdm(tickers, desc=f"Fetching stocks' information")
    for ticker in progress_bar:
        try:
            stock_info = get_stock_info(ticker, obi_strict)
            if stock_info:
                stocks_info.append(stock_info)
        except Exception as e:
            print(f"{ticker} Error: ", e)
            continue

    stocks_info_df = pd.DataFrame(stocks_info)
    stocks_info_df.insert(stocks_info_df.shape[1], 'OBI',
                          stocks_info_df.apply(is_obi, axis=1))

    # order alphabetically
    companies_info_df = stocks_info_df.sort_values(by=['Ticker'])

    return companies_info_df


def export_stock_info(stocks_info_df: pd.DataFrame, output_name: str):
    """
    Save the stocks information to an Excel file
    :param stocks_info_df: dataframe of stocks information
    :param output_name: name of the output file
    :return:
    """
    today_date = datetime.datetime.now().strftime("%Y_%m_%d")
    stocks_info_df.to_excel(f"{output_name}_{today_date}.xlsx")
    print(f"Stocks information saved to {output_name}_{today_date}.xlsx")


def main(output_name: str, obi_strict: bool = False):
    # get  tickers
    tickers = get_tickers()

    # get companies info
    stocks_info_df = get_stocks_info(tickers, obi_strict)

    # save the stocks information to an Excel file
    export_stock_info(stocks_info_df, output_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract stock information')
    parser.add_argument('-iex-token', help='Your IEX token')
    parser.add_argument('-output', help='Output file name')
    parser.add_argument('-OBI-strict', help='Whether to use strict OBI criteria')
    args = parser.parse_args()

    MY_TOKEN = args.iex_token
    output_file = args.output if args.output is not None else 'stocks_info'
    obi_strict = args.OBI_strict if args.OBI_strict is not None else False
    main(output_file, obi_strict)
