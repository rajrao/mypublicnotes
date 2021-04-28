@dataclass
class MyDataClass:
    fred: int
    jim: int
    sheila: int

    def __post_init__(self):
        if self.fred < 0:
            raise ValueError
