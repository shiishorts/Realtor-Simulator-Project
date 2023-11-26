from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import json
from extruct import JsonLdExtractor
import time


class House:
    def __init__(self, url, price):
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


# returns adj hosues for BFS and DFS
def get_adjacent_houses(house, all_houses):
  adjacency_threshold = 50

  house_price = int(house.price.replace('$', '').replace(',', ''))

  return [other_house for other_house in all_houses
  if house != other_house
  and abs(int(other_house.price.replace('$', '').replace(',', '')) - house_price) <= adjacency_threshold]


def dfs_traverse_houses(houses, preferred_rent):
  preferred_rent = int(preferred_rent)
  
  stack = []
  visited_houses = set()
  rent_range = 50    # return houses within a $50 range from preferred rent
  matching_houses = []
  
  for house in houses:
      if house not in visited_houses:
          stack.append(house)
          visited_houses.add(house)  # mark as visited
  
          while stack:
              current_house = stack.pop()  # last house from the stack
  
              # Remove dollar sign and commas before converting to int
              house_price = int(current_house.price.replace('$', '').replace(',', ''))
  
              # check if within range rent
              if preferred_rent - rent_range <= house_price <= preferred_rent + rent_range:
                  matching_houses.append(current_house)
  
              neighbors = get_adjacent_houses(current_house, houses)
  
              for neighbor in neighbors:
                  if neighbor not in visited_houses:
                      stack.append(neighbor)
                      visited_houses.add(neighbor)
  
  return matching_houses



# 11/22/2023 MONICA
def bfs_traverse_houses(houses, preferred_rent):
  # make into int
  preferred_rent = int(preferred_rent)
  
  # *** I just had it return all houses within $50 range ***
  rent_range = 50
  
  queue = deque(houses)
  visited_houses = set()    # TODO: make sure we can use sets LOL
  
  matching_houses = []
  
  while queue:
      current_house = queue.popleft()

      if current_house in visited_houses:
        continue
  
      # change house's price to an int
      house_price = int(current_house.price.replace('$', '').replace(',', ''))
  
      # check if the house's price is within preferred rent range
      if preferred_rent - rent_range <= house_price <= preferred_rent + rent_range:
          matching_houses.append(current_house)


      adjacent_houses = get_adjacent_houses(current_house, houses)
    
      queue.extend(adjacent_houses)

      visited_houses.add(current_house)
  
  return matching_houses



# 11/22/2023 MONICA
def compare_bfs_dfs(houses, preferred_rent):
  start_time_bfs = time.time()
  bfs_result = bfs_traverse_houses(houses, preferred_rent)
  end_time_bfs = time.time()

  start_time_dfs = time.time()
  dfs_result = dfs_traverse_houses(houses, preferred_rent)
  end_time_dfs = time.time()

  print(f"\nBFS took {end_time_bfs - start_time_bfs:.2f} seconds.")
  print(f"DFS took {end_time_dfs - start_time_dfs:.2f} seconds.")

  if bfs_result == dfs_result:
      return bfs_result
  else:
      print("Results from BFS and DFS do not match.")
      return None
      


if __name__ == '__main__':
  #variables
  university = input("Enter the university name: ")
  city = input("Enter the city name: ")
  url = 'https://www.forrentuniversity.com/'#does not change

  headers = {
      'authority':
          'www.forrentuniversity.com',
      'user-agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'
  }  # used to access the website [sends a signal saying that a computer is trying to access it]

  #menu1 stuff (get uni, city)
  url = makeURL(url, university, city) #string of url
  listHouses = getHousingList(url, headers) #array of House [use for BFS and DFS]
  

  #menu2 stuff (price one)
  # 11/22/2023 MONICA
  while True:
    print("1. Display All Houses")
    print("2. Find Housing")

    choice = input("Enter your choice: ")

    if choice == "1":
        for house in listHouses:
          print(house)

    elif choice == "2":
        preferred_rent = input("Enter your preferred monthly rent: $")
        print("\nFinding Housing:")
        houses_result = compare_bfs_dfs(listHouses, preferred_rent)

        if houses_result:
            print("\nHouses found within a $50 rent range:")
            for house in houses_result:
                print(house)
              
    else:
        print("Invalid choice. Try again.")
