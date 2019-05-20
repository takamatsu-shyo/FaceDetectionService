# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

import requests
import json
import cv2
import time

addr = 'http://localhost:5000'
test_url = addr + '/test'
facedetect_url = addr + '/facebox'


# Prepare headers for http request
content_type = 'image/jpeg'
headers      = {'content-type': content_type}

# Read and decode a image
img = cv2.imread('./photo/jaak_id.jpg')
_, img_encoded = cv2.imencode('.jpg', img)

# Test: Send HTTP request with image and recieve response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
print (json.loads(response.text))


# FaceDetect: Send HTTP request with image and recieve response
response = requests.post(facedetect_url, data=img_encoded.tostring(), headers=headers)
print (json.loads(response.text))


