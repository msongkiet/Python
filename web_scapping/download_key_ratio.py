# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# %%
df = pd.read_csv('symbol.csv', header=[0], index_col=None)
lst_symbol = df['symbol'].tolist()
print(len(lst_symbol))


# %%
driver=webdriver.Chrome(executable_path="C:\\chromedriver_win32\\chromedriver.exe")
driver.quit()


# %%
class MyDriver(object):
    def __init__(self, driver, default_timeout=2):
        self.driver = driver
        self.timeout = default_timeout

    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

mydriver = MyDriver(driver)


# %%
mydriver=webdriver.Chrome(executable_path="C:\\chromedriver_win32\\chromedriver.exe")
mydriver.maximize_window()

for symbol in lst_symbol:
    url = f'http://financials.morningstar.com/ratios/r.html?t={symbol}&region=tha&culture=en-US'
    print(url)
    mydriver.get(url)
    mydriver.find_element_by_class_name('large_button').click()
    print("------------ Downloaded ------------")

print("Completed")
mydriver.quit()

# %%



