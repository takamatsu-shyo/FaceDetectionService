import requests
url = 'http://localhost:8000/post'
files = {'media': open('yaris.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.text)
