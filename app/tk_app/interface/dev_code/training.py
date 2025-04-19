from bs4 import BeautifulSoup
from requests_html import HTMLSession

if __name__ == '__main__':
    session = HTMLSession()

    response = session.get('https://haddan.novikovproject.ru/maze?level=1')

    response.html.render(sleep=3)

    soup = BeautifulSoup(response.html.html, 'lxml')

    map = soup.find(class_='maze-map__content')

    print(map.prettify())
