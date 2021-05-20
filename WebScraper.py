from urllib.request import urlopen as uReq
import csv
import bs4
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import tqdm
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

    # Key:
    # 0) Name
    # 1) CPU
    # 2) GPU
    # 3) Display
    # 4) HDD/SSD
    # 5) RAM
    # 6) OS
    # 7) Dimensions
    # 8) Weight
    # 9) Body material
    # 10) M.2 Slot
    # 11) Misc
    # 12) USB Type-A
    # 13) USB Type-C
    # 14) HDMI
    # 15) VGA
    # 16) DVI
    # 17) Card reader
    # 18) Lan
    # 19) Wi-Fi
    # 20) Audio jack
    # 21) Web camera
    # 22) Microphone
    # 23) Speakers
    # 24) Optical drive
    # 25) Security Lock Slot
    # 26) Fingerprint reader
    # 27) Backlit keyboard
    # 28) Bluetooth
    labels = ["Name", "CPU", "GPU", "Display", "HDD/SSD", "RAM", "OS", "Dimensions", "Weight", "Body material",
              "M.2 Slot", "Misc", "USB Type-A", "USB Type-C", "HDMI", "VGA", "DVI", "Card reader", "Ethernet Lan",
              "Wi-Fi", "Audio jack", "Web camera", "Microphone", "Speakers", "Optical drive", "Security lock slot",
              "Fingerprint reader", "Backlit keyboard", "Bluetooth"]
    laptops = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
              [], [], [], []]

    #Make into for loop
    for i in tqdm.tqdm(range(len(links))):
    #for i in tqdm.tqdm(range(4)):
        try:
            driver.get(links[i])
            page_html = driver.page_source
            page_soup = soup(page_html, 'html.parser')
            laptop = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                      [], [], [], []]
            laptop[0].append(page_soup.find("h1", text=True).text)

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
                # Default specifications
                for element in sub_soup.find_all("div", {"class": "col-md-8"}):
                    if div.strong.text == "Display":
                        laptop[3].append(str(element.text).strip("\n").strip(" "))
                    elif div.strong.text == "HDD/SSD":
                        laptop[4].append(str(element.text).strip("\n").strip(" "))
                    elif div.strong.text == "RAM":
                        laptop[5].append(str(element.text).strip("\n").strip(" "))
                    elif div.strong.text == "OS":
                        laptop[6].append(str(element.text).strip("\n").strip(" "))
                    elif div.strong.text == "Dimensions":
                        laptop[7].append(str(element.text).strip("\n").strip(" "))
                    elif div.strong.text == "Weight":
                        laptop[8].append(str(element.text).strip("\n").strip(" "))
                    elif div.strong.text == "Body material":
                        laptop[9].append(str(element.text).strip("\n").strip(" "))
                    elif div.strong.text == "M.2 Slot":
                        laptop[10].append(str(element.text).strip("\n").strip(" "))
                    else:
                        laptop[11].append(str(element.text).strip("\n").strip(" "))

                # CPU and GPU
                for element in sub_soup.find_all("div", {"class": "col-md-10"}):
                    if div.strong.text == "GPU":
                        gpu_names = str(element.text).strip("\n").strip(" ")
                    elif div.strong.text == "CPU":
                        cpu_names = str(element.text).strip("\n").strip(" ")

                for element in sub_soup.findAll("a", href=True):
                    embedded_links.append(element['href'])

            divs2 = page_soup.find_all("div", {"class": "lp-row-double-table"})
            for div in divs2:
                sub_soup2 = soup(str(div), "html.parser")
                # Ports and connectivity
                for element in sub_soup2.find_all("li"):
                    subsub_soup2 = soup(str(element), "html.parser")
                    if element['class'][0] == "icon-usb-a":
                        laptop[12].append(str(element.text).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-usb-c":
                        laptop[13].append(str(element.text).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-hdmi":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[14].append("Yes")
                        else:
                            laptop[14].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-vga":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[15].append("Yes")
                        else:
                            laptop[15].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-dvi":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[16].append("Yes")
                        else:
                            laptop[16].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-card-reader":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[17].append("Yes")
                        else:
                            laptop[17].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-lan":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[18].append("Yes")
                        else:
                            laptop[18].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-wi-fi":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[19].append("Yes")
                        else:
                            laptop[19].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-audio-jack":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[20].append("Yes")
                        else:
                            laptop[20].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-web-camera":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[21].append("Yes")
                        else:
                            laptop[21].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-microphone":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[22].append("Yes")
                        else:
                            laptop[22].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-speakers":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[23].append("Yes")
                        else:
                            laptop[23].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-dvd":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[24].append("Yes")
                        else:
                            laptop[24].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-security-lock":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[25].append("Yes")
                        else:
                            laptop[25].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-finger-print":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[26].append("Yes")
                        else:
                            laptop[26].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-backlight":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[27].append("Yes")
                        else:
                            laptop[27].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))
                    elif element['class'][0] == "icon-bluetooth":
                        if len(subsub_soup2.find_all("i")) > 0:
                            laptop[28].append("Yes")
                        else:
                            laptop[28].append(str(subsub_soup2.find("em").string).strip("\n").strip(" "))

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
                            cpu_specification[str(names[0].string)] = str(value[0].string).strip(" ")
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
                            gpu_specification[str(names[0].string)] = str(value[0].string).strip(" ")
                        counter += 1

                gpu_specifications.append(gpu_specification)

            laptop[1].append(cpu_specifications)
            laptop[2].append(gpu_specifications)

            for i in range(len(laptop)):
                if len(laptop[i]) == 0:
                    laptop[i].append("none")
                laptops[i].append(laptop[i])

        except:
            continue

    #Saving to a csv file
    myFile = open('data.csv', 'w')
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
