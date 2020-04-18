# VideoEdit

A tiny command-line python software for video resizing and video image overlaying.

## Usage 

Help message : 

```
usage: main.py [-h] [-O VIDEO IMAGE] [-R VIDEO_PATH RATIO] [-W IMAGE] [-e end_time] [-b begin_time] [-o OUTPUT_FILE] [-c X Y]

optional arguments:
  -h, --help            show this help message and exit
  -O VIDEO IMAGE, --overlay VIDEO IMAGE
                        Overlays an image into the provided video
  -R VIDEO_PATH RATIO, --resize VIDEO_PATH RATIO
                        Resizes a video with the provided ratio (0.5 for half of the original size)
  -W IMAGE, --webcam_overlay IMAGE
                        Overlays an image into a webcam stream
  -e end_time, --end end_time
                        Superior time limit for image overlay into video (in seconds)
  -b begin_time, --begin begin_time
                        Inferior time limit for image overlay into video (in seconds)
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Output file (default : out.avi)
  -c X Y, --coords X Y  Overlay coords (in pixels)
  ```
  
## Examples 
  
  * Overlay an image (image.png) into a pre-existing video (video.mp4) at coordinates (0; 250), between 10 and 15 seconds, with abc.avi as output file :
    ```$ python3 main.py --overlay 'video.mp4' 'image.png' --output 'abc.avi' -b 10 -e 15 --coord 0 250```
  * Overlay an image (image.png) into a webcam stream, at coordinates (0; 250), with abc.avi as output file:
    ```$ python3 main.py --webcam_overlay 'image.png' --output 'abc.avi' --coord 0 250```
  * Resize a video with a 0.5 ratio (half the original size of the video. This ratio can be between 0 and 100, where 100 is 100 times the original size of the video), with abc.avi as output file :
    ```$ python3 main.py --resize 'video.mp4' 0.5 --output 'abc.avi' ```
  
