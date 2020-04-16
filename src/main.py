import time
import argparse
import sys
from functions import *

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-O', '--overlay', nargs=2, type=str, metavar=('VIDEO', 'IMAGE'))
    parser.add_argument('-e', '--end', nargs=1, type=int, metavar='end_time', default=[0])
    parser.add_argument('-b', '--begin', nargs=1, type=int, metavar='begin_time', default=[0])
    parser.add_argument('-o', '--output', nargs=1, type=str, metavar="OUTPUT_FILE", default="out.avi")
    parser.add_argument('-c', '--coords', nargs=2, type=int, metavar=("X", "Y"), default=[0, 0])
    args = parser.parse_args()
    
    begin_time = time.time()
    if args.overlay:
        video_overlay(args.overlay[0], args.overlay[1], args.begin[0], args.end[0], args.output, args.coord[0], args.coord[1])
    else:
        print("[!] No action specified - Exiting...")

    print(f"Execution finished in {round(time.time() - begin_time)}s")


if __name__ == "__main__":
    main()
