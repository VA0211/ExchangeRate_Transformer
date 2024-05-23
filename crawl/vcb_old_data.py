import pandas as pd
from datetime import timedelta, date
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def get_exchange_rate_by_day(date_str):
    # Initialize Chrome WebDriver
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # Load the page
    driver.get("https://portal.vietcombank.com.vn/en-Us/Corporate/TG/Pages/exchange-rate.aspx?devicechannel=default")

    # Find the date input element and clear existing value
    date_input = driver.find_element(By.ID, "txttungay")
    date_input.clear()

    # Enter the new date
    date_input.send_keys(date_str)
    date_input.send_keys(Keys.RETURN)

    sleep(1)  # Wait for the page to load

    # Extract data from the page
    table = driver.find_element(By.CLASS_NAME, "tbl-01")
    rows = table.find_elements(By.TAG_NAME, "tr")

    exchange_rates = []
    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 5:
            continue  # Skip rows that don't have enough cells
        currency_name = cells[0].text.strip()
        currency_code = cells[1].text.strip()
        buy_cash = cells[2].text.strip().replace(',', '')
        buy_transfer = cells[3].text.strip().replace(',', '')
        sell = cells[4].text.strip().replace(',', '')
        exchange_rates.append({
            'Date': date_str,
            'Currency Name': currency_name,
            'Currency Code': currency_code,
            'Buy Cash': buy_cash,
            'Buy Transfer': buy_transfer,
            'Sell': sell
        })

    # Close the WebDriver
    driver.quit()

    return pd.DataFrame(exchange_rates)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def crawl_data(start_date, end_date):
    crawl_list = []
    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime('%d/%m/%Y')
        print(f"Getting data for date {date_str}")
        df_crawl = get_exchange_rate_by_day(date_str)
        if df_crawl is not None:
            crawl_list.append(df_crawl)
        sleep(1)
    if crawl_list:
        df = pd.concat(crawl_list, ignore_index=True)
        return df
    else:
        return None

def main():
    start_date = date(2019, 1, 1)
    end_date = date(2019, 2, 1)

    df_vnd = crawl_data(start_date, end_date)
    if df_vnd is not None:
        df_vnd.to_csv('../crawl/data/vcb/2019/vcb_rates_2019_1.csv', index=False, header=True)
    else:
        print("Exchange rates not found for the given date range")

if __name__ == "__main__":
    main()