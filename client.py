# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

import requests
import json
import cv2

addr = 'http://localhost:5000'
test_url = addr + '/facebox'

# Prepare headers for http request
content_type = 'image/jpeg'
headers      = {'content-type': content_type}

img = cv2.imread('./photo/jaak_id.jpg')

# Encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)

# Send HTTP request with image and recieve response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

# Decode response
print (json.loads(response.text))

