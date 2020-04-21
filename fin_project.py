#################################
##### Name: Gloria Gyakari  #####
##### Uniqname: ggyakari    #####
#################################

from bs4 import BeautifulSoup
import requests
import json
from xml.etree import ElementTree


class WorldBank: #Change to world bank
    '''a national site 
    #Change to world bank

    Instance Attributes
    -------------------
    topic: string
        the topics on the WB site that has to do with country development (e.g. 'Education', '')
        some countries have topics the WB focuses on.

    country: string
        the name of a country (e.g. 'Ghana') 
    '''
    
    def __init__(self, country, capital, population, currencies, languages, subregion, country_id):
        self.country = country
        self.capital = capital
        self.population = population
        self.currencies = currencies
        self.languages = languages
        self.subregion = subregion
        self.country_id = country_id
  
    def info(self):
        print (self.country + " is located within " + self.subregion +'. ' + self.capital + " is the capital city and the country has a population of "  + str(self.population)) 
        print('The currencies used in ' + self.country + ' are: ')
        for currency in self.currencies:
          print(currency['name'] + ' ' + currency['symbol'])
        print('The languages used in ' + self.country + ' are: ')
        for language in self.languages:
          print(language['name']) 
        

def convert_to_dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  This dict representation includes meta data such as the object's module and class names.
  """
  
  #  Populate the dictionary with object meta data 
  obj_dict = {
    "__class__": obj.__class__.__name__,
    "__module__": obj.__module__
  }
  
  #  Populate the dictionary with object properties
  obj_dict.update(obj.__dict__)
  
  return obj_dict

#https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
def dict_to_obj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")
        
        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")
        
        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)
        
        # Get the class from the module
        class_ = getattr(module,class_name)
        
        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj

def load_cache():
    try:
        cache_file = open('cache.json', 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache):
    cache_file = open('cache.json', 'w')
    contents_to_write = json.dumps(cache,indent=4)
    cache_file.write(contents_to_write)
    cache_file.close()

#https://restcountries.eu/rest/v2/name/{name}
def teleport_data(country):
    url = 'https://restcountries.eu/rest/v2/name/' + country + '?fullText=true'
    response = requests.get(url)
    data = load_cache()
    response.raise_for_status()
    return (response.json())

def rankings(number):
    if number == 1:
      url = 'https://www.theglobaleconomy.com/rankings/health_spending_per_capita/'
      response = requests.get(url)
      soup= BeautifulSoup(response.text, 'html.parser')
      rankings = soup.find_all('div',{ 'class' : 'outsideTitleElement' })
      rankings = soup.find_all('a',{ 'class' : 'graph_outside_link' })
      for i in range(len(rankings)):
        print(i+1, rankings[i].text)
    elif number == 2:
      url = 'https://www.theglobaleconomy.com/rankings/Life_expectancy/'
      response = requests.get(url)
      soup= BeautifulSoup(response.text, 'html.parser')
      rankings = soup.find_all('div',{ 'class' : 'outsideTitleElement' })
      rankings = soup.find_all('a',{ 'class' : 'graph_outside_link' })
      for i in range(len(rankings)):
        print(i+1, rankings[i].text)
    elif number == 3:
      url = 'https://www.theglobaleconomy.com/rankings/prisoners/'
      response = requests.get(url)
      soup= BeautifulSoup(response.text, 'html.parser')
      rankings = soup.find_all('div',{ 'class' : 'outsideTitleElement' })
      rankings = soup.find_all('a',{ 'class' : 'graph_outside_link' })
      for i in range(len(rankings)):
        print(i+1, rankings[i].text)
    elif number == 4:
      url = 'https://www.theglobaleconomy.com/rankings/human_rights_rule_law_index/'
      response = requests.get(url)
      soup= BeautifulSoup(response.text, 'html.parser')
      rankings = soup.find_all('div',{ 'class' : 'outsideTitleElement' })
      rankings = soup.find_all('a',{ 'class' : 'graph_outside_link' })
      for i in range(len(rankings)):
        print(i+1, rankings[i].text)

def wb_topics(number, country):
    if number == 1:
      url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/annualavg/bccr_bcm2_0/tas/1980/1999/' + country.country_id
      response = requests.get(url)
      print('According to the Bergen Climate Model from the time-period of 1980 - 1999, the average annual temperature, in degrees Celsius was ' + str(round(response.json()[0]['annualData'][0],3)))
    elif number == 2:
      print(1)
    elif number == 3:
      response =  requests.get('http://api.worldbank.org/v2/country/' +  country.country_id[0:2]+'/indicator/NY.GDP.MKTP.CD?date=2006')
      response.raise_for_status()
      tree = ElementTree.fromstring(response.content)
      print('The GDP of Ghana as of World Bank data from the year 2006 is \n$ ' + tree.find('.//{http://www.worldbank.org}value').text)
    elif number == 4:
      url = 'http://api.worldbank.org/v2/country/' + country.country_id[0:2] + '?format=json'
      response = requests.get(url)
      print('Average Income Level in ' + country.country + ': ' + response.json()[1][0]['incomeLevel']['value'])

def initialize():
  url = 'https://api.teleport.org/api/countries/'
  uurl = 'https://www.worldbank.org/en/where-we-work'
  response = requests.get(url)
  rresponse = requests.get(uurl)
  soup= BeautifulSoup(rresponse.text, 'html.parser')
  countries = soup.find("div", class_="alpha-list-section")
  countries = soup.find_all('li', {'class': 'alpha-name'})
  apiResponse = response.json()['_links']['country:items']
  dict = {}
  for item in apiResponse:
    dict[item['name']] = [item['href'][-15:]]
    print('Processing....')
  for item in countries:
    try:
      dict[item.find("a").text].append(item.find("a")["href"])
    except KeyError:
      dict[item.find("a").text] = [item.find("a")["href"]]  

  return dict



if __name__ == "__main__":
  
  while True:
    cache = load_cache()
    url = 'https://api.teleport.org/api/countries/'
    if url in cache.keys():
      print("Using cache")

    else:
      print('-------------------------------------------')
      print('      COMPILING LISTS OF COUNTRIES         ')
      print('-------------------------------------------')
      print('Fetching')
      cache[url] = initialize()
      save_cache(cache)
    print('-------------------------------------------')
    print('               COUNTRIES                   ')
    print('-------------------------------------------')
    country = input('Enter a country name or exit: \n')
    if country in cache.keys():
      print("\nUsing cache")
      obj = dict_to_obj(cache[country])
      obj.info()
    else:
      print('\nFetching')
      info = teleport_data(country)
      obj = WorldBank(info[0]['name'],info[0]['capital'],info[0]['population'],info[0]['currencies'],info[0]['languages'], info[0]['subregion'], info[0]['alpha3Code'])
      obj.info()
      cache[country] = convert_to_dict(obj)
      save_cache(cache)
    print('-------------------------------------------')
    print('                TOPICS                     ')
    print('-------------------------------------------')
    print('\nWhat topics would you like to explore about this country');
    print('1. Climate \n2. Education \n3. Finances \n4. Income Level')
    topics = int(input('Pick a topic: \n'))
    wb_topics(topics, obj)
    print('-------------------------------------------')
    print('                RANKINGS                     ')
    print('-------------------------------------------')
    print('\nWhat rankings would you like to explore:');
    print('1. Health spending per capita  \n2. Life expectancy \n3. Imprisonment rate  \n4. Human Rights Index ')
    ranking = int(input('Pick a rankings: \n'))
    rankings(ranking)
    
    
   


