import os
import io

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_details(filename, coin):
    with io.open(filename, 'w',encoding="utf-8") as f:
        f.write("Value: " + coin.value + '\n')
        f.write("Country/Region: " + coin.country + '\n')
        f.write("Year/Years: " + str(coin.years) + '\n')
        f.write("Metal: " + coin.metal + '\n')
        f.write("Type: " + coin.coin_type + '\n')
        f.write("Weight: " + coin.weight + '\n')
        f.write("Diameter: " + coin.diameter + '\n')
        f.write("Shape: " + coin.shape + '\n')
        f.write("References: " + str(coin.references) + '\n')
        f.write("Rarity: " + coin.rarity + '\n')
        f.write("Demonetized: " + coin.demonetized + '\n')
        f.write("Link: " + coin.link + '\n')
