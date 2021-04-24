from pydantic.dataclasses import dataclass #only change was to add pydantic.
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
    strawberries = 'strawberries'


@dataclass
class IceCreamMix:
        name: str
        flavor: Flavor
        toppings: Tuple[Topping,...] #Tuple[str,...]
        scoops: int

def main():
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

    try:
        iceCreamMix2 = IceCreamMix(
            "PB&J Bad",
            "bad butter",
            ("Bad Topping"),
            2       
        )
        print(iceCreamMix2)
    except Exception as err:
        print(err.json())

if __name__ == '__main__':
    main()