@dataclass(
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
)
class MyDataClass:
    fred: int
    jim: int
    sheila: int
