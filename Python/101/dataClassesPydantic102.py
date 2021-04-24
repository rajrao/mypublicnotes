from pydantic import BaseModel,Field,validator,root_validator,ValidationError #changed to BaseModel
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

class Container(str, Enum):
    cup='cup'
    waffle='waffle'
    waffle_cup = 'waffle cup'

#@dataclass #decorator has to be removed.
class IceCreamMix(BaseModel):
        name: str
        flavor: Flavor
        toppings: Tuple[Topping,...] #Tuple[str,...]
        scoops: int = Field(...,gt=0,lt=5)

        @validator('toppings')
        def check_toppings(cls, toppings):
            if len(toppings) > 2:
                raise ValueError('Too many toppings')
            return toppings

        @root_validator
        def check_cone_toppings(cls, values):
            container = values.get('container')
            toppings = values.get('toppings')
            if container == Container.waffle_cup and Topping.hot_fudge in toppings:
                raise ValueError("Hot fudge cant be used on waffle cones")
            return values


def main():
    iceCreamMix = IceCreamMix(
        name= "PB&J",
        flavor = "peanut butter",
        toppings = ("strawberries","sprinkles"),
        scoops = 2       
    )
    print(iceCreamMix)

    iceCreamMix2 = IceCreamMix(
        name = "PB&J",
        flavor = Flavor.peanut_butter,
        toppings = (Topping.hot_fudge,Topping.cookies),
        scoops = 2       
    )
    print(iceCreamMix2.json()) #json support

    iceCreamReconstituted = IceCreamMix.parse_raw('''
    {
        "name": "PB&J Parsed", 
        "flavor": "peanut butter", 
        "toppings": ["hot fudge", "cookies"], 
        "scoops": 2
    }
    ''')
    print(iceCreamReconstituted.json())

    try:
        iceCreamMix2 = IceCreamMix(
            name = "PB&J Bad",
            flavor = "bad butter",
            toppings = ("Bad Topping"),
            scoops = 200       
        )
        print(iceCreamMix2)
    except ValidationError as err:
        print(err.json())

if __name__ == '__main__':
    main()