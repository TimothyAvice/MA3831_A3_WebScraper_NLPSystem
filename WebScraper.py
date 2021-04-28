from urllib.request import urlopen as uReq

import bs4
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    website_url = 'https://laptopmedia.com/au/all-laptop-series/'

    number_of_pages = 50

    driver = webdriver.Chrome()

    all_laptops = []
    all_laptop_info = []

    driver.get(website_url)

    page_html = driver.page_source

    driver.quit()

    page_soup = soup(page_html, 'html.parser')

    laptops = page_soup.findAll("a", {"class":"lp-series-table-row"})

    print(len(laptops))


main()
