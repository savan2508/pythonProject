'''
http://quotes.toscrape.com/page/2/. 
Use what you know about for loops and string concatenation to loop through all the pages and get all the unique authors on
the website. Keep in mind there are many ways to achieve this, also note that you will need to somehow 
figure out how to check that your loop is on the last page with quotes. For debugging purposes, 
I will let you know that there are only 10 pages, so the last page is http://quotes.toscrape.com/page/10/, 
but try to create a loop that is robust enough that it wouldn't matter to know the amount of pages beforehand, 
perhaps use try/except for this, its up to you!
'''

import bs4
import requests
import lxml


page_still_valid = True
authors = set()
url = 'http://quotes.toscrape.com/page/'
page =1

while page_still_valid:
    
    page_url = url+str(page)
    
    res = requests.get(page_url)
    
    if 'No quotes found!' in res.text:
        break
    
    soup = bs4.BeautifulSoup(res.text,'lxml')
    
    for name in soup.select(".author"):
        authors.add(name.text)

    page += 1
        
for i in authors:
    print(i)