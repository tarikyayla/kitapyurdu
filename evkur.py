from bs4 import BeautifulSoup as bs 
import requests
from tqdm import tqdm


HOST = "http://www.evkur.com.tr"
req = requests.get("http://www.evkur.com.tr/telefon").text
soup = bs(req,"html.parser")


items = soup.select("div.innerTop_productsSec")
urunler = []
kategoriler = []
for cat_id,cat in tqdm(enumerate(items[0].find_all("li")),total=len(items[0].find_all("li"))) :
    kategori_ismi = cat.find("p").text
    kategori_link = cat.find("a")["href"]
    kategoriler.append(kategori_ismi)
    req = requests.get(HOST+kategori_link).text
    ss = bs(req,"html.parser")
    liste = ss.select("div.grid_viewSec")[0].find_all("li")
    for item in liste:
        try:
            urun_gorseli = item.select("div.imgWrapper > a > img")[0]["src"]
            urun_gorseli = urun_gorseli.replace("165.jpeg","550.jpeg")
            urun_ismi = item.select("div.discription > h4 > a")[0].text
            fiyat = float(item.select("div.bottom_price > div.fr > p ")[0].text.strip().replace(" TL","").replace(".","").replace(",","."))
            urunler.append({
                "catId" : (cat_id+1),
                "urunGorsel": urun_gorseli,
                "urunName":urun_ismi,
                "fiyat" : fiyat
            })
        except Exception as identifier:
            pass
