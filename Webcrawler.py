import requests
from bs4 import BeautifulSoup
import re
import Files

from bs4 import  NavigableString
from bs4 import  Tag

def scan_url_return_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup

def get_tuple_country_link(oject):
    all_coins = oject.findAll("ul", {"class": "liste_pays"})[0]
    list1 = all_coins.findChildren("li", recursive=False)
    countries = []
    for i in list1:
        j = re.findall('title="(.+)".+href="(.+)"', str(i), flags=re.I)
        countries.append(j[0])

    return countries

def advanced_search(country):
    new_url = r"/index.php?mode=avance&p=1&l="+country+"&r=&e="+country\
              +"&d=&ca=3&no=&i=&v=&m=&a=&t=&dg=1800-&w=&u=&f=&g=&tb=y&tc=y&tn=y&tp=y&tt=y&te=y&cat=y"
    return new_url


url = "https://en.numista.com/catalogue/pays.php"
soup_obj = scan_url_return_soup(url)
countries = get_tuple_country_link(soup_obj)

print(len(countries))

print(countries)
#Files.create_dir("countries")

url2 = 'https://en.numista.com/catalogue/'
more_results_on_page = "?q=100"
first_country_tuple = countries[0]
urll = first_country_tuple[1]

def get_ccountry_url(url):
    a = url.split(".")[0]
    return a[:-1]

def get_numer_of_pages(url):
    soup2 = scan_url_return_soup(url2 + url+ more_results_on_page)
    aaa = soup2.findAll("div", {"class": "catalogue_navigation"})[0]
    j = re.findall('(\d+)\s+coins\s+found', str(aaa), flags=re.I)
    return j


print(get_numer_of_pages(urll))
# country_url = first_country_tuple[1]
# strr = get_ccountry_url(urll)
# print(strr)
# print(first_country_tuple)
# soup2 = scan_url_return_soup(url2+first_country_tuple[1]+more_results_on_page)
# print(url2+first_country_tuple[1]+more_results_on_page)
# print(first_country_tuple[0])
# print(soup2)
#
# aaa = soup2.findAll("div", {"class": "catalogue_navigation"})
# print("####")
# print(aaa)