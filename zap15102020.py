import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver import DesiredCapabilities

chromedriver = "C:/chromedriver"
date_begin = str(input('ввести начальную дату формат 01.01.2020 '))
date_end = str(input('ввести конечную дату формат 01.01.2020 '))
region = 'г. Москва'
urls = []


def first(url):
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    driver.find_element_by_id('ctl00_cphBody_mdsMessageType_imgSelect').click()
    sleep(3)
    driver.switch_to.frame(0)
    driver.find_element_by_xpath("//li[9]/div/span[2]").click()
    driver.find_element_by_xpath("//li[9]/ul/li/div/span[2]").click()
    driver.switch_to.default_content()
    element = driver.find_element_by_id("ctl00_cphBody_cldrBeginDate_tbSelectedDate")
    actions = ActionChains(driver)
    actions.double_click(element).perform()
    driver.find_element_by_id("ctl00_cphBody_cldrBeginDate_tbSelectedDate").send_keys(date_begin)
    element = driver.find_element_by_xpath("//td[5]/table/tbody/tr/td/input")
    actions = ActionChains(driver)
    actions.double_click(element).perform()
    driver.find_element_by_id("ctl00_cphBody_cldrEndDate_tbSelectedDate").send_keys(date_end)
    dropdown = driver.find_element_by_id("ctl00_cphBody_ucRegion_ddlBoundList")
    dropdown.find_element_by_xpath("//option[. = 'г. Москва']").click()
    driver.find_element_by_id("ctl00_cphBody_ibMessagesSearch").click()
    sleep(2)
    r = driver.find_elements_by_xpath("//a[contains(text(),'Объявление о проведении торгов')]")
    for i in r:
        a = i.get_attribute('href')
        urls.append(str(a))


first("https://bankrot.fedresurs.ru/Messages.aspx")


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome_driver = webdriver.Chrome(chromedriver, options=options)
    chrome_driver.implicitly_wait(1)
    return chrome_driver


res = pd.DataFrame()

for url2 in urls:
    driver = init_driver()
    driver.get(url2)
    element_list = driver.find_elements_by_xpath('//table[@class="lotInfo"]')
    element_html = element_list[0].get_attribute('innerHTML')
    if "кв.м" in element_html or "кв. м" in element_html or "ЕГРН" in element_html or 'кадастр' in element_html:
        pd.set_option('display.width', None)
        df_list = pd.read_html(f'<table>{element_html}</table>')
        df = df_list[-1]
        df["URL"] = url2
        res = pd.concat([res, df])

    else:
        continue

res.to_csv('bank.csv', sep=';', encoding='cp1251')






