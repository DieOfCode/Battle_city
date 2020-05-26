#!/usr/bin/env python3
import argparse
from screen import screen

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--game', '-G', action='store_const', const='1', help='This will be option One')
    # if parser.parse_args().game == '1':
    screen = screen.Screen()
    screen.start_screen()
