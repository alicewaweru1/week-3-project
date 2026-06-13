import requests

url = 'http://books.toscrape.com/index.html'

response = requests.get(url)

print(response.status_code)

#print(response.content)