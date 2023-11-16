from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import json
from extruct import JsonLdExtractor

if __name__ == '__main__':
    headers = {
        'authority': 'www.forrentuniversity.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0',
    }

    response = requests.get('https://www.forrentuniversity.com/', headers=headers)
    response2 = requests.get('https://www.forrentuniversity.com/University-of-Florida-Gainesville', headers=headers)
    #print(response2) -> prints respnose code [404] if it does not exist

    #print(response2.headers)
    #print(response2.text)


    soup = BeautifulSoup(response2.text, "html.parser")
    something = soup.find(type="application/ld+json")

    data = JsonLdExtractor().extract(response2.text)
    #print(data[0])

    print(data[0].get("about")) #gets the list of apartments in about

    for s in data:
        for a in s:
            print(a)
