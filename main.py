from bs4 import BeautifulSoup as bs
import requests
import json

link = "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=2&filter_in_stock=1&filter_in_stock=1&limit=100"

class Kitap:
    def __init__(self,kitap_adi,yazar_adi,yayinevi,kapak,desc,link,fiyat):
        self.kitap_adi = kitap_adi
        self.yazar_adi = yazar_adi
        self.yayinevi = yayinevi
        self.kapak = kapak
        self.desc = desc
        self.link = link
        self.fiyat = fiyat

req = requests.get(link).text
soup = bs(req,"html.parser")

kitaplar = soup.find_all("div",{"itemtype":"http://schema.org/Book"})

array = []
for kitap in kitaplar:
    try:
        cover_div = kitap.find("div",{"class":"cover"})
        link = cover_div.find("a").get("href")
        kapak = cover_div.find("img").get("src")
        kitap_adi = cover_div.find("img").get("alt")
        yayinevi = kitap.find("div",{"class":"publisher"}).find("a").text
        yazar_adi = kitap.find("div",{"class":"author"}).find("a").text.lstrip(' ')
        desc = kitap.find("div",{"class":"product-info"}).text
        fiyat = kitap.find("div",{"class":"price-new "}).find("span",{"class":"value"}).text.lstrip(' ')
        array.append(Kitap(kitap_adi,yazar_adi,yayinevi,kapak,desc,link,fiyat))
    except Exception as e:
        pass
        #Bazı kitapların yazar kısmı boş.



def exportAsJSON(array, filename):
	with open(filename + ".json", "w+") as writer:
		writer.write("[")
		for x, kitap in enumerate(array):
			writer.write(json.dumps(kitap.__dict__, indent=4, ensure_ascii=False))
			if(x != len(array)-1): writer.write(",")
		writer.write("]")

exportAsJSON(array,"kitapyurdu")