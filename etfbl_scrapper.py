import requests
import codecs
import re

import unicodecsv as csv
import pandas as pd

from bs4 import BeautifulSoup

NEWS_LINK = "http://old.etfbl.net/?c=prikazi&objekat=oglas"


page = requests.get(NEWS_LINK)
if page.status_code == 200:
    print "Page downloaded successfully"
    soup = BeautifulSoup(page.content, 'html.parser')


### Example 1
    with codecs.open("output.html", "wb", encoding='utf8') as file:
        file.write(soup.prettify())

### Example 2
    news = soup.find_all('a', class_='silentlink')
    with codecs.open("output2.html", "wb", encoding='utf8') as file:
        for entry in news:
            if entry.has_attr('href'):
                file.write(entry.get_text()+"\n")
                file.write(NEWS_LINK+entry['href']+"\n")

### Example 3
#   Important note, since python 2.7 default csv doesn't hande unicode we had to import unicodecsv as csv
#   Also this requires adding additional parameter encoding to csv.writer function as welll as
#   using pyhon open, instead of codecs open required for earlier examples
###
    with open("output3.csv", "wb") as file:
        res = {}
        for idx, entry in enumerate(news):
            #previousSibling element in same level as current element
            res[idx] = {}
            res[idx]["link"] = NEWS_LINK+entry['href']
            # parent is td and sibling is td with date text
            res[idx]["date"] = entry.parent.previousSibling.get_text()
            res[idx]["text"] = entry.get_text()

        writer = csv.writer(file, delimiter=",", encoding='utf-8')
        writer.writerow(["name", "link", "date"])
        for a in range(len(res.keys())):
            writer.writerow([res[a]["text"], res[a]["link"], res[a]["date"]])

### Example 4
    #news2 = soup.find_all('a', href=True, text='[RSS]')
    news2 = soup.find_all('a', href=re.compile('.*f_ploca=7$'))
    entries2 = news2[0].parent.findNext('table').findChildren('td', class_=False)
    dates2 = news2[0].parent.findNext('table').findChildren('td', class_="podtekst")
    dates = []
    links = []
    texts = []
    for i in range(len(dates2)):
        dates.append(dates2[i].get_text())
    for i in range(len(entries2)):
        if i % 2 == 0:
            link = entries2[i].findChildren('a')[0]
            links.append(NEWS_LINK+link['href'])
            texts.append(link.get_text())
    res2 = pd.DataFrame({
        "dates": dates,
        "links": links,
        "texts": texts})
    res2.to_csv('output4.csv',encoding='utf8')
