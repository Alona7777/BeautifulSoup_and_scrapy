import requests
import json
from bs4 import BeautifulSoup


base_url = 'http://quotes.toscrape.com'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'lxml')

AUTHORS = []
QUOTES =[]
authors_data = 'authors.json'
quotes_data = 'quotes.json'

def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml') 
    return soup

def get_authors_urls(soup: BeautifulSoup):
    urls = []
    about_links = soup.find_all('a', text='(about)')

    # get urls
    for link in about_links:
        l = link['href']
        url = f'{base_url}{l}'
        urls.append(url)
    return urls

def get_authors(urls: list) -> list:
    authors = []
    for url in urls:
        soup = get_soup(url)
        author = {}
        author['fullname'] = soup.find('h3', class_='author-title').text
        author['born_date'] = soup.find('span', class_='author-born-date').text
        author['born_location'] = soup.find('span', class_='author-born-location').text
        author['description'] = soup.find('div', class_='author-description').text.strip()
        authors.append(author)
    return authors

def get_tags(soup: BeautifulSoup) -> list:
    tags_quotes = []
    quotes = soup.find_all('div', class_='quote')
    for q in quotes:
        tag_quote = {}
        tags = q.find('meta', class_='keywords')
        if tags:
            keywords_content = tags.get('content').split(',')
            tag_quote['tags'] = keywords_content
        tag_quote['author'] = q.find('small', itemprop='author').text
        tag_quote['quote'] = q.find('span', class_='text').text
            
        tags_quotes.append(tag_quote)
    return tags_quotes

def write_to_json(data: str, result: list):
    with open(data, 'w', encoding='utf-8') as fd:
        json.dump(result, fd, ensure_ascii=False, indent=2)

def all_page_urls(url, urls=None):
    if urls is None:
        urls = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    check_next = soup.find('li', class_='next')
    if check_next:
        next_page_url = soup.select('li.next a')[0].get('href')
        get_next_url = f'{base_url}{next_page_url}'
        urls.append(get_next_url)
        all_page_urls(get_next_url, urls)
  
    return urls

def scrape_page(soup: BeautifulSoup):
    authors_url = get_authors_urls(soup)
    authors = get_authors(authors_url)
    AUTHORS.append(authors)
    quotes = get_tags(soup)
    QUOTES.append(quotes)

def main():
    base_soup = get_soup(base_url)
    scrape_page(base_soup)
    all_urls = all_page_urls(base_url)
    for elem in all_urls:
        elem_soup = get_soup(elem)
        scrape_page(elem_soup)
    
    authors = []
    for element in AUTHORS:
        for el in element:
            authors.append(el)

    quotes = []
    for element in QUOTES:
        for el in element:
            quotes.append(el)
 
    write_to_json(authors_data, authors)
    write_to_json(quotes_data, quotes)


if __name__ == '__main__':
    main()
