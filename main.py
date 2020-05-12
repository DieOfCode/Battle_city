#!/usr/bin/env python3
import argparse
from screen import Screen

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--game','-G', action='store_const', const='1', help='This will be option One')
    # if parser.parse_args().game == '1':
    screen = Screen.Screen()
    screen.start_screen()
