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
    #{"Name": [], "Specifications": {"CPU": [{}], "GPU": [{}], "Display": "",
    # "HDD/SSD": "", "M.2 Slot": "", "RAM": "", "OS": "",
    # "Dimensions": "", "Weight": "", "Body Material": "", "Ports and conductivity": "", "Features": ""}}

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

    #Make into for loop
    for link in links:
        laptop = {}
        driver.get(link)
        page_html = driver.page_source
        page_soup = soup(page_html, 'html.parser')

        laptop["Name"] = page_soup.find("h1", text=True).text

        specifications = {}
        cpu_specifications = []
        gpu_specifications = []
        embedded_links = []
        gpu_links = []
        cpu_links = []
        cpu_names = ""
        gpu_names = ""

        divs = page_soup.find_all("div", {"class": "lp-row-table lp-row-table-inline"})
        for div in divs:
            sub_soup = soup(str(div), 'html.parser')
            for element in sub_soup.find_all("div", {"class": "col-md-8"}):
                specifications[div.strong.text] = str(element.text).strip("\n").strip(" ")
            for element in sub_soup.find_all("div", {"class": "col-md-10"}):
                if div.strong.text == "GPU":
                    gpu_names = str(element.text).strip("\n").strip(" ")
                elif div.strong.text == "CPU":
                    cpu_names = str(element.text).strip("\n").strip(" ")
            for element in sub_soup.findAll("a", href=True):
                embedded_links.append(element['href'])

        cpu_names = cpu_names.split(",")
        gpu_names = gpu_names.split(",")

        for link in embedded_links:
            if "https://laptopmedia.com/au/processor" in link:
                cpu_links.append(link)
            elif "https://laptopmedia.com/au/video-card" in link:
                gpu_links.append(link)

        # Another for loop nested for each cpu
        for cpu_link in cpu_links:
            driver.get(cpu_link)
            page_html = driver.page_source
            page_soup = soup(page_html, 'html.parser')

            cpu_specification = {}
            cpu_specification["CPU_name"] = cpu_names[0]

            counter = 0
            divs = page_soup.find_all("div", {"class":"col-md-6 col-sm-12"})
            for div in divs:
                sub_soup = soup(str(div), 'html.parser')
                tables = sub_soup.findChildren('table')
                my_table = tables[0]
                rows = my_table.findChildren(['th', 'tr'])
                for row in rows:
                    value = row.findChildren('td')
                    names = row.findChildren('th')
                    if len(value) > 0 and counter > 0:
                        cpu_specification[names[0].string] = str(value[0].string).strip(" ")
                    counter += 1

            cpu_specifications.append(cpu_specification)

        # Another for loop nested for each gpu
        for gpu_link in gpu_links:
            driver.get(gpu_link)
            page_html = driver.page_source
            page_soup = soup(page_html, 'html.parser')

            gpu_specification = {}
            gpu_specification["GPU_name"] = gpu_names[0]

            counter = 0
            divs = page_soup.find_all("div", {"class": "col-md-6 col-sm-12"})
            for div in divs:
                sub_soup = soup(str(div), 'html.parser')
                tables = sub_soup.findChildren('table')
                my_table = tables[0]
                rows = my_table.findChildren(['th', 'tr'])
                for row in rows:
                    value = row.findChildren('td')
                    names = row.findChildren('th')
                    if len(value) > 0 and counter > 0:
                        gpu_specification[names[0].string] = str(value[0].string).strip(" ")
                    counter += 1

            gpu_specifications.append(gpu_specification)

        specifications["CPU"] = cpu_specifications
        specifications["GPU"] = gpu_specifications

        laptop["Specifications"] = specifications

        laptops.append(laptop)


main()
