from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import json
from extruct import JsonLdExtractor
import time


class House:
    def __init__(self, price, url):
        self.price = price
        self.url = url

    def __str__(self):
        return "fPrice: {self.price}, URL: {self.url}"


def makeURL(site, university, city):  # puts together the url and returns url
    word_temp = university.split()  # split the input into just words

    for i in word_temp:  # iterate through the list of singular words
        site = site + i + '-'  # add it to string url

    site = site + city  # add in city
    return site


# idea is that when call DFS and BFS functions, we call thru measureTime to calculate time ran
# def measureTime(func, *args):
#   start_time = time.time()
#   result = func(*args)    # call function, store result
#   end_time = time.time()
#   print(f"{func.__name__} took {end_time - start_time:.4f} seconds.")
#   return result

def getHousingList(site, header):
    response = requests.get(url=site, headers=header)
    # print(response) -> prints response code [404] if it does not exist
    # -> prints [200] if exists
    data = JsonLdExtractor().extract(response.text)  # list of breadcrumb information

    temp = data[0].get("about")  # gets the list of apartments in the about section of the breadcrumb

    # empty array to store housing information
    houses = []

    # puts houses into an array
    for h in temp:
        houseURL = h.get("url")

        # repeat process for each apartment complex
        response = requests.get(url=houseURL, headers=header)
        data = JsonLdExtractor().extract(response.text)
        temp = data[0].get("about")
        price = temp.get("priceRange").split()[0]  # get the price (lower bound)

        houses.append(House(houseURL, price))  # create and add house to array

    return houses  # return houses


if __name__ == '__main__':
    # variables
    university = "university of florida"
    city = "gainesville"
    url = 'https://www.forrentuniversity.com/'

    headers = {
        'authority':
            'www.forrentuniversity.com',
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'
    }  # used to access the website [sends a signal saying that a computer is trying to access it]

    # menu1 stuff (get uni, city)
    url = makeURL(url, university, city)

    listHouses = getHousingList(url, headers)

    # menu2 stuff (price one)
