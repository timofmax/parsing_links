import csv
from bs4 import BeautifulSoup
import requests
import re


def data_to_dump():
    with open('output_file.csv', 'w') as f:
        start_page = int(input("start page to parse: "))
        end_page = int(input("last page to parse: "))
        writer = csv.writer(f)
        main_sps = []
        regex = re.compile("commentbody-\d+")
        site = "http://www.digitaltut.com/share-your-route-v2-0-experience/comment-page-{}#comments"
        for i in range(start_page, end_page):
            source = requests.get(site.format(i)).text
            soup = BeautifulSoup(source, "lxml")
            date = soup.find_all("div", class_="date")
            message = soup.find_all(id=regex)
            author = soup.find_all("div", class_="author")
            for d, m, a in zip(date, message, author):
                sps = []
                d = d.text.strip() #date of message
                m = m.text.strip() #message themself
                a = a.text.strip() #nickname of post's author
                if "http" in m:
                    msg = m
                    m = m.split('\n')
                    sps_mini = [] #lists of links only
                    [sps_mini.append(i.replace(" ","")) for i in m if "http" in i]
                    sps.append(msg)
                    sps.append("\n".join(sps_mini))
                    sps.append(d)
                    sps.append(a)
                    main_sps.append(sps)
                else:
                    pass
        for row in main_sps:
            writer.writerow(row)

if __name__ == '__main__':
    data_to_dump()
