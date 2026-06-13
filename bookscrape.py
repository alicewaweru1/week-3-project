import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'http://books.toscrape.com/index.html'

response = requests.get(url)

print(response.status_code)

#print(response.content)

soup = BeautifulSoup(response.content, 'html.parser')

cards = soup.select('.product_pod')
print(cards[0])
all_the_books = []
for card in cards:
    title = card.select_one('h3 a').text
    print(title)
    price = card.select_one('.price_color').text
    description = card.select_one('p').text
    print(price)
    
    book_item = {
        'title': title,
        'price': price,
        'description': description
    }
    all_the_books.append(book_item)
#print(all_the_books)
df = pd.DataFrame(all_the_books)
#df.to_csv('scraped_books.csv',)
df.to_excel('scraped_books.xlsx',)

