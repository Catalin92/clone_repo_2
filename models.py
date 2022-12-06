class Coin:

    def __init__(self, country, years, value, metal, coin_type, weight, diameter, shape, rarity, demonetized, link, references):
        self.country = country
        self.years = years
        self.value = value
        self.metal = metal
        self.coin_type = coin_type
        self.weight = weight
        self.diameter = diameter
        self.shape = shape
        self.references = references
        self.rarity = rarity
        self.demonetized = demonetized
        self.link = link




    def get_rarity(self):
        return self.rarity


    def __str__(self):
        return f'Country: {self.country}\nValue: {self.value}\nYear: {self.years}\nMetal: {self.metal}' \
               f'\nReferences: {self.references}\nType: {self.coin_type}\nWeight: {self.weight}\nRarity: {self.rarity}'





