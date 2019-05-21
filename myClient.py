#
# What?   : Command line interface for FaceDetction server
# How to ?: python3 myClient your_image.jpg -f
# Ref     : https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594
# Comment : Don't foreget to run the server before you fire this script
#

import requests
import json
import cv2
import time
import argparse
import os.path
import sys

# Arg parser
parser = argparse.ArgumentParser()
parser.add_argument("jpg", help="JPEG image to send GPU server")
parser.add_argument("-f", "--face", action="store_true", help="face detection")
args = parser.parse_args()

print('Input image: ', args.jpg)
 
if(os.path.isfile(args.jpg)):
   # Read and decode a image
    img = cv2.imread(args.jpg)
    _, img_encoded = cv2.imencode('.jpg', img)

else:
    # Exit
    sys.exit('JPEG File not found', args.jpg )

addr = 'http://localhost:5000'
test_url = addr + '/test'
facedetect_url = addr + '/facebox'

# Prepare headers for http request
content_type = 'image/jpeg'
headers      = {'content-type': content_type}

# Test: Send HTTP request with image and recieve response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
print (json.loads(response.text))

# FaceDetect: Send HTTP request with image and recieve response
# Only with -f option
if args.face:
   response = requests.post(facedetect_url, data=img_encoded.tostring(), headers=headers)
   print (json.loads(response.text))


