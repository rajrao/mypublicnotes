from dataclasses import dataclass

from position import Position, EarthPosition


@dataclass(eq=True, frozen=False)
class Location:
    name: str
    position: Position

    def __post_init__(self):
        if self.name == "":
            raise ValueError("Location name cannot be empty")


hong_kong = Location("Hong Kong", EarthPosition(22.29, 114.16))
stockholm = Location("Stockholm", EarthPosition(59.33, 18.06))
cape_town = Location("Cape Town", EarthPosition(-33.93, 18.42))
rotterdam = Location("Rotterdam", EarthPosition(51.96, 4.47))
maracaibo = Location("Maracaibo", EarthPosition(10.65, -71.65))
