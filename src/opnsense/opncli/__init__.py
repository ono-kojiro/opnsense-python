from .usage import *
from .apikey import read_apikey

def main():
    from .cli import main as cli_main
    return cli_main()

