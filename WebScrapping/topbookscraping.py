import requests
import bs4
import lxml

""" This script do the web scrapping from the toscrape.com website and download
a list of the books that has a two star rating"""

base_url = 'http://books.toscrape.com/catalogue/page-{}.html' #get website url

two_star_titles = []

for n in range(1,51):

    scrape_url = base_url.format(n)
    page = requests.get(scrape_url)

    soup = bs4.BeautifulSoup(page.text,'lxml')
    books = soup.select('.product_pod')

    for book in books:

        if len(book.select('.star-rating.Two')) != 0:
            book_title = book.select('a')[1]['title']
            two_star_titles.append(book_title)

print(two_star_titles)