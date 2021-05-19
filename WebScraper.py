from urllib.request import urlopen as uReq

import bs4
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    website_url = 'https://laptopmedia.com/au/all-laptop-series/'

    driver = webdriver.Chrome()

    driver.get(website_url)

    page_html = driver.page_source

    page_soup = soup(page_html, 'html.parser')

    links = []
    for a in page_soup.findAll("a", {"class":"lp-series-table-row"}, href=True):
        links.append(a['href'])

    # For each laptop it will have the following structure
    #{"Name": [], "Specifications": {"CPU": [{}], "GPU": [{}], "Display": [],
    # "HDD/SSD": "", "M.2 Slot": "", "RAM": "", "OS": "",
    # "Dimensions": "", "Weight": "", "Body Material": "", "Ports and conductivity": {}, "Features": {}}}

    # For each CPU
    # {"Name": "", "Frequency": "", "Cores": "", "Instruction type": "", "TDP": "", "Max Temp": "", "Memory channels": "",
    # "Released": "", "Architecture": "", "Threads": "", "LL Cache": "", "Lithography": "", "Max GPU Frequency": "",
    # "Memory Type": "", "Max memory": ""}

    # For each GPU
    # {"Name": "", "Manufacturing Process": "", "Architecture": "", "Base frequency": "", "Memory Type": "",
    # "Memory Frequency": "", "Memory bandwidth": "", "Released": "", "Power consumption": "", "Cores": "",
    # "Maximum frequency": "", "Memory Capacity": "", "Memory bus": ""}

    # For each Display
    # Direct text copy

    laptops = []
    for link in links:
        driver.get(link)
        page_html = driver.page_source
        page_soup = soup(page_html, 'html.parser')


    CPU_links = []
    GPU_links = []
    disp_links = []


main()
