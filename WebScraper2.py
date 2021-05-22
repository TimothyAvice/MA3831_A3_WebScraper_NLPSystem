import csv
import bs4
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import tqdm

# Chromedriver version 90 required to be installed


def main():

    # Get all the link for each laptop
    website_url = 'https://www.notebookcheck.net/Reviews.55.0.html?&items_per_page=500&hide_youtube=1&ns_show_num_normal=1&hide_external_reviews=1&introa_search_title=laptop%20review&tagArray[]=16&typeArray[]=1'

    driver = webdriver.Chrome(executable_path=r"C:\Users\Timothy\Documents\chromedriver.exe")

    driver.get(website_url)

    page_html = driver.page_source

    page_soup = soup(page_html, 'html.parser')

    links = []
    for a in page_soup.findAll("a", {"class": "introa_large introa_review"}, href=True):
        links.append(a['href'])
    for a in page_soup.findAll("a", {"class": "introa_small introa_review"}, href=True):
        links.append(a['href'])

    website_url = "https://www.notebookcheck.net/Reviews.55.0.html?&items_per_page=500&hide_youtube=1&ns_show_num_normal=1&hide_external_reviews=1&page=1&introa_search_title=laptop%20review&tagArray[]=16&typeArray[]=1"

    driver.get(website_url)

    page_html = driver.page_source

    page_soup = soup(page_html, 'html.parser')

    for a in page_soup.findAll("a", {"class": "introa_large introa_review"}, href=True):
        links.append(a['href'])
    for a in page_soup.findAll("a", {"class": "introa_small introa_review"}, href=True):
        links.append(a['href'])

    labels = ["Title", "Intro", "Specifications", "Case", "Connectivity", "Input devices", "Display", "Performance",
              "Emissions", "Energy management", "Verdict"]
    laptops = [[], [], [], [], [], [], [], [], [], [], []]
    # Make into for loop
    for i in tqdm.tqdm(range(len(links))):
    # for i in tqdm.tqdm(range(1)):
        try:
            driver.get(links[i])
            page_html = driver.page_source
            page_soup = soup(page_html, 'html.parser')
            laptop = [[], [], [], [], [], [], [], [], [], [], []]
            laptop[0].append(page_soup.find("h1", text=True).text)
            laptop[1].append(str(page_soup.find("div", {"class": "intro-text"}).contents[1]).strip(" "))
            temp = page_soup.find('div', {"class": "csc-textpic-text"}).findAll(text=True)

            # Retrieve Intro information
            for item in temp:
                str(item).strip(" ").replace('\n', '')
            temp = " ".join(temp).replace("  ", " ")
            laptop[1][0] = laptop[1][0] + " " + temp

            divs = page_soup.find_all("div", {"class": "ttcl_0 csc-default"})
            counter = 2
            for div in divs[1:]:
                sub_soup = soup(str(div), 'html.parser')
                if len(sub_soup.find_all("h2")) > 0:
                    counter += 1

                try:
                    sub_temp = sub_soup.find('div', {"class": "csc-textpic-text"}).findAll(text=True)
                    for item in sub_temp:
                        str(item).strip(" ").replace('\n', '')

                    laptop[counter].append(str(" ".join(sub_temp).replace("  ", " ")))
                    laptop[counter][0].strip('\n', '').replace("  ", " ")
                except:
                    continue

            for i in range(len(laptop)):
                if len(laptop[i]) == 0:
                    laptop[i].append("none")
                laptops[i].append(laptop[i])

        except:
            continue

    # Saving to a csv file
    myFile = open('data2.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(labels)
        for i in tqdm.tqdm(range(len(laptops[0]))):
            try:
                laptop = []
                for j in range(len(laptops)):
                    laptop.append(laptops[j][i][0])
                writer.writerow(laptop)
            except:
                continue

main()