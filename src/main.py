import time
import argparse
import sys
from functions import *

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-O', '--overlay', nargs=2, type=str, metavar="INPUT_FILES")
    parser.add_argument('-e', '--end', nargs=1, type=int, metavar='end_time', default=0)
    parser.add_argument('-b', '--begin', nargs=1, type=int, metavar='begin_time', default=0)
    parser.add_argument('-o', '--output', nargs=1, type=str, metavar="OUTPUT_FILE", default="out.avi")
    args = parser.parse_args()
    
    begin_time = time.time()
    if args.overlay:
        video_overlay(args.overlay[0], args.overlay[1], args.begin, args.end, args.output)

    print(f"Execution finished in {round(time.time() - begin_time)}s")


if __name__ == "__main__":
    main()
