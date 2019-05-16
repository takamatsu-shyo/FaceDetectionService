# POST Python
# https://docs.vendhq.com/docs/image-upload-sample-python
# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

# POST curl
# https://davidwalsh.name/curl-post-file


import requests
url = 'http://localhost:8000/post'
files = {'media': open('yaris.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.text)
