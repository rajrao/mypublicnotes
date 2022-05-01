from enum import Enum

#more colors: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
class Color(Enum):
    DEFAULT = '\033[39m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
def printC(color:Color= Color.DEFAULT, msg: str = ''):
    print(f'{color.value}{msg}{Color.DEFAULT.value}')
