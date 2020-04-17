import time
import argparse
import sys
import os
from overlay import *
from resize import *

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-O', '--overlay', nargs=2, type=str, metavar=('VIDEO', 'IMAGE'))
    parser.add_argument('-R', '--resize', nargs=1, type=str, metavar="VIDEO_PATH")
    parser.add_argument('-r', '--ratio', nargs=1, type=float, metavar='RATIO', default=[0])
    parser.add_argument('-x', '--conserve_ratio', action='store_true')
    parser.add_argument('-e', '--end', nargs=1, type=int, metavar='end_time', default=[0])
    parser.add_argument('-b', '--begin', nargs=1, type=int, metavar='begin_time', default=[0])
    parser.add_argument('-o', '--output', nargs=1, type=str, metavar="OUTPUT_FILE", default=["out.avi"])
    parser.add_argument('-c', '--coords', nargs=2, type=int, metavar=("X", "Y"), default=[0, 0])
    args = parser.parse_args()
    
    begin_time = time.time()
    if os.path.isfile(args.output[0]):
        return print("[X] The specified output already exists ! Please change the -o/--output argument value")
    if args.overlay:
        video_overlay(args.overlay[0], args.overlay[1], args.begin[0], args.end[0], args.output[0], args.coords[0], args.coords[1])
    elif args.resize:
        resize_video(args.resize[0], args.output[0], args.ratio[0], args.conserve_ratio)
    else:
        print("[!] No action specified - Exiting...")

    print(f"Execution finished in {round(time.time() - begin_time)}s")


if __name__ == "__main__":
    main()
