from dataclasses import dataclass
from typing import Tuple
from enum import Enum

class Flavor(str, Enum):
    chocolate = 'chocolate'
    vanilla = 'vanilla'
    strawberry = 'strawberry'
    peanut_butter = 'peanut butter'

class Topping(str, Enum):
    sprinkles = 'sprinkles'
    hot_fudge = 'hot fudge'
    cookies = 'cookies'


@dataclass
class IceCreamMix:
        name: str
        flavor: Flavor
        toppings: Tuple[Topping,...] #Tuple[str,...]
        scoops: int

def main():
    #Dataclass does not provide any validation
    iceCreamMix = IceCreamMix(
        "PB&J",
        "peanut butter",
        ("strawberries","sprinkles"),
        2       
    )
    print(iceCreamMix)

    iceCreamMix2 = IceCreamMix(
        "PB&J",
        Flavor.peanut_butter,
        (Topping.hot_fudge,Topping.cookies),
        2       
    )
    print(iceCreamMix2)

if __name__ == '__main__':
    main()