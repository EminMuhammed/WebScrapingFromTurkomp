import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.turkomp.gov.tr/database?type=foods"


def get_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def product_urls(soup):
    column = soup.find("table", attrs={"id": "mydatalist"})
    rows = column.find_all("tr", attrs={"rol": "row"})
    urls = ["http://www.turkomp.gov.tr/" + row.a.get("href") for row in rows]
    return urls


def parse_table(tr_list):
    liste_icerik = []
    for tr in tr_list:
        bilesenadi = tr.find_all("td")[0].text.strip()
        birim = tr.find_all("td")[1].text.strip()
        ortalama = tr.find_all("td")[2].text
        min = tr.find_all("td")[3].text
        max = tr.find_all("td")[4].text

        print(bilesenadi)
        print(birim)
        print(ortalama)
        print(min)
        print(max)
        print("*****************")
        sozluk = {"bilesenadi": bilesenadi,
                  "birim": birim,
                  "ortalama": ortalama,
                  "min": min,
                  "max": max}
        # liste_icerik.append([bilesenadi, birim, ortalama, min, max])
        liste_icerik.append(sozluk)
    return liste_icerik


def parse_products(product_urls):
    liste = []

    for url in product_urls:
        print(url)
        soup = get_content(url)
        product_name = soup.find("label", attrs={"class": "col-sm-12 control-label"}).text.strip()
        table = soup.find("table", attrs={"id": "foodResultlist"}).find("tbody")

        tr_all = table.find_all("tr")
        print(product_name)
        liste_icerik = parse_table(tr_all)
        liste.append([product_name, liste_icerik])
        print("------------------------------------------------------")

    return liste


def save_excel(content):
    df = pd.DataFrame(content)
    df.to_excel("D:/GİTHUB REPO/Scraping/BesinDegerleri/besindegerleri.xlsx")


soup = get_content(url)
urls = product_urls(soup)
liste = parse_products(urls)
save_excel(liste)
