import requests
from bs4 import BeautifulSoup
import re
from models import Coin
import urllib.request
import time
from functools import partial
import os
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from Files import create_dir, write_details

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
        j = re.findall('title="(.+?)".+href="(.+)"', str(i), flags=re.I)
        countries.append(j[0])
    print(countries)
    print(len(countries))
    return countries

def advanced_search(country, page_number=1):
    new_url = r"index.php?mode=avance&p="+ str(page_number)+ "&l="+country+"&r=&e="+country\
              +"&d=&ca=3&no=&i=&v=&m=&a=&t=&dg=1800-&w=&u=&f=&g=&tb=y&tc=y&tn=y&tp=y&tt=y&te=y&cat=y"
    return new_url

def iterate_over_pages(country, page_number):
    s = "https://en.numista.com/catalogue/"+ r"index.php?mode=avance&p="+ str(page_number)+ "&l="+country+"&r=&e="+country\
              +"&d=&ca=3&no=&i=&v=&m=&a=&t=&dg=1800-&w=&u=&f=&g=&tb=y&tc=y&tn=y&tp=y&tt=y&te=y&cat=y" + "&q=100"
    return s

def get_countryString_in_url(url):
    a = url.split(".")[0]
    a = a.replace("/catalogue/","")
    return a[:-2]

def get_numer_of_coins(url, country):
    more_results_on_page = "?q=100"
    print("url is ", url + country + more_results_on_page)
    soup2 = scan_url_return_soup(url + country + more_results_on_page)
    catalogue = soup2.findAll("div", {"class": "catalogue_navigation"})
    if not catalogue:
        return "0"
    j = re.findall('(\d+)\s+(?:results|result)\s+found', str(catalogue[0]), flags=re.I)
    print("Number of coins is: ")
    print(catalogue[0])
    return j[0]

def calc_pages(coins):
    if coins <= 100:
        return 1
    else:
        if coins % 100 == 0:
            return coins // 100
        else:
            return coins // 100 + 1

##################################################



def fooo(country):
    name = country[0]
    country_url = country[1]
    print("Name of country: " + name + "; URL: " + country_url)
    country_part = get_countryString_in_url(country_url)
    print(advanced_search(country_part))
    nr_of_coins = get_numer_of_coins(url, advanced_search(country_part))
    print(country_part + " : " + nr_of_coins)
    if int(nr_of_coins) > 0:
        create_dir(r"countries\\"+str(name))
    else:
        return
    nr_pages = calc_pages(int(nr_of_coins))

    # url_coin = iterate_over_pages(country=country_part, page_number=1)
    # print(" link " + url_coin)
    print("pages : " + str(nr_pages))

    for i in range(1, nr_pages+1):
        url_coin = iterate_over_pages(country=country_part, page_number=i)
        print("##########")
        print(url_coin)

        scaned = scan_url_return_soup(url_coin)

        all_coins = scaned.findAll("div", {"id": "resultats_recherche"})[0]
        list1 = all_coins.findAll("div", {"class": "resultat_recherche"})

        loo = []
        for i in list1[:-1]:
            j = re.findall('href="(.+\.html)"', str(i), flags=re.I)
            loo.append(j[0])

        p = ThreadPool(5)
        # aa = p.map(extract_info_and_create_coin, loo[0:1])
        aa = p.map(partial(extract_info_and_create_coin, country = name), loo)

        # for i in loo:
        #     extract_info_and_create_coin(i,name)



def checking_regex(result):
    # print(result)
    if len(result) == 0:
        return 'NA'
    else:
        return result[0]

def create_coin(string, country, link, rarity):
    reg = re.findall('<th>(?:Years|Year)<\/th>\s+<td>(.+|\n.+)<\/td>', string, flags=re.I)
    years = checking_regex(reg)
    years = years.replace(" ", "")
    years = years.replace("\n", "")
    print("*****************************")
    print(years)
    # reg = re.findall('<th>Value<\/th>\s+<td[\s\S]+?>([\s\S]+?)(?:\(|<)', string, flags=re.I)
    reg = re.findall('<th>Value<\/th>\s+<td>([\s\S]+?)<', string, flags=re.I)

    value = checking_regex(reg).replace("\n", "")
    value = " ".join(value.split()).replace("/", "-")
    if '<' in value or '>' in value:
        value = value.replace('>', '')
        value = value.replace('<', '')
    if '"' in value:
        value = value.replace('"','')
    value = value.replace("&amp;nbspAFA", "")
    print(value)
    reg = re.findall('<th>Composition</th>\s+<td>(.+)</td>', string, flags=re.I)
    metal = checking_regex(reg)
    print(metal)
    reg = re.findall('<th>Type</th>\s+<td>(.+)</td>', string, flags=re.I)
    coin_type = checking_regex(reg)
    print(coin_type)
    reg = re.findall('<th>Weight</th>\s+<td>(.+)</td>', string, flags=re.I)
    weight = checking_regex(reg).replace(r"x\a0", "")
    print(weight)
    reg = re.findall('<th>Diameter</th>\s+<td>(.+)</td>', string, flags=re.I)
    diameter = checking_regex(reg).replace(r"x\a0", "")
    print(diameter)
    reg = re.findall('<th>Shape</th>\s+<td>(.+)</td>', string, flags=re.I)
    shape = checking_regex(reg)
    print(shape)
    reg = re.findall('<th>References</th>[\s\S]+?KM</abbr>([\s\S]+?)<', string, flags=re.I|re.M)
    references = checking_regex(reg).replace(",", "").replace("#", "").replace("?", "").strip()

    reg = re.findall('<th>Demonetized</th>\s+<td>(.+)</td>', string, flags=re.I)
    demonetized = checking_regex(reg)
    print(demonetized)
    coin = Coin(country, years, value, metal, coin_type, weight, diameter, shape, rarity, demonetized, link, references)
    return coin


def extract_info_and_create_coin(soup_str, country):
    url1 = "https://en.numista.com" + soup_str
    soup = scan_url_return_soup(url1)

    reg = re.findall("numista\s+rarity\s+index:\s+<\w+>(\d+)", str(soup), flags=re.I | re.M)
    rarity = checking_regex(reg)

    caract = soup.findAll("section", {"id": "fiche_caracteristiques"})[0]
    object = caract.findChildren("tr")
    string = str(object)
    unique_nr = soup_str[:-5]
    unique_nr = unique_nr.replace("/catalogue/", "")

    coin = create_coin(string, country, url1, rarity)

    coin_folder = 'countries\\' + country + f'\\{coin.value}_{coin.years}_{coin.references}__{unique_nr}'

    print(coin_folder)
    create_dir(coin_folder)
    write_details(coin_folder + "\\Details.txt", coin)

    if 'pieces43649' in soup_str:
        print("eroaaaaareeee")
        return
    photo_list = soup.findAll("div", {"id": "fiche_photo"})
    if len(photo_list) > 0:
        photo = photo_list[0]
    else:
        print("No photo for coin "+ coin.value)
        return

    photo1 = photo.findAll("a", {"data-fluidbox": ""})
    print(coin.country, coin.value, coin.years, coin.rarity, coin.references)

    if(len(photo1) == 0):
        return

    if 'obverse' in str(photo1[0]):
        avers = re.findall('src="(.+?)"', str(photo1[0]), flags=re.I)
        urllib.request.urlretrieve(avers[0], coin_folder + '\\avers.png')
    if  len(photo1) > 1 and 'reverse' in str(photo1[1]):
        revers = re.findall('src="(.+?)"', str(photo1[1]), flags=re.I)
        urllib.request.urlretrieve(revers[0], coin_folder + '\\revers.png')





if __name__ == '__main__':
    print("######################")
    url = "https://en.numista.com/catalogue/"
    soup_obj = scan_url_return_soup(url + "pays.php")
    countries = get_tuple_country_link(soup_obj)
    print(len(countries))
    x = time.time()
    p = ThreadPool(5)
    # aa = p.map(fooo, countries[0:4])
    # fooo(countries[114])
    # fooo(countries[113])
    aa = p.map(fooo, countries[240:245])
    # aa = p.map(fooo, countries[240:-2])
    y= time.time()
    print(y-x)