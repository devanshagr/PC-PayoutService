import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.asxenergy.com.au/futures_au"
DELAY = 5 # seconds
STATE_NAME = "New South Wales"
QUARTER_DATA = "BQtr"
Q4_DATA = "Q423"
PATH_TO_FILE = "Data/Future_Price.txt"

market_dataset_xpath = "//div[@class='market-dataset']"
parent_xpath = "//div[@class='market-dataset']//table//tbody//tr//td[@class='market-dataset-state']"
child_parent_xpath = "//td[@class='market-dataset-state']//div[@class='dataset']//table//thead//tr//td[@class='instrument']"
qtr_data_xpath = "//td[@class='market-dataset-state']//div[@class='dataset']//table//tbody//tr//td[@class='instrument']"
# qtr_settle_data_xpath = "td[@class='settle']"
qtr_settle_data_xpath = "td[7]"


def save_price_to_file(data):
    f = open(PATH_TO_FILE, "w")
    f.write(json.dumps(data))
    f.close()

def get_future_price():

    driver = webdriver.Chrome('./chromedriver')
    driver.get(URL)

    myElem = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, parent_xpath)))

    market_dataset_entries = driver.find_elements(by=By.CLASS_NAME, value="market-dataset")

    header = market_dataset_entries[0]
    state_data = market_dataset_entries[1]

    all_headers = header.find_elements(By.XPATH, parent_xpath)

    for i, header in enumerate(all_headers):
        if header.text == STATE_NAME:
            index_to_consider = i

    all_state_data = state_data.find_elements(By.XPATH, parent_xpath)

    nsw_state_data = all_state_data[index_to_consider+4]

    nsw_state_data_types = nsw_state_data.find_elements(By.XPATH, child_parent_xpath)

    for each_nsw_state_data_type in nsw_state_data_types:
        if each_nsw_state_data_type.text == QUARTER_DATA:
            corresponding_table_body = each_nsw_state_data_type.find_element(By.XPATH, '../../..')
            all_instrs = corresponding_table_body.find_elements(By.XPATH, qtr_data_xpath)
            for instr in all_instrs:
                if instr.text == Q4_DATA:
                    corresponding_tr = instr.find_element(By.XPATH, '..')
                    future_price = corresponding_tr.find_element(By.XPATH, qtr_settle_data_xpath).text
                    break

    print (future_price)
    data = {
        "future_price": future_price
    }
    
    # save_price_to_file(data)

    return data

if __name__ == "__main__":
    get_future_price()


