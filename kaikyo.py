import re
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://kaikyoujp1.com/sp.html'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    td_list = soup.find_all('td')

    for td in td_list:
        item_data = dict()
        text = td.text
        if not text:
            continue

        text = text.replace('\n', '').replace('\u3000', '').replace(',', '')
        text = ' '.join([string for string in text.split(' ') if string]).strip()

        price = re.findall(r'￥([0-9]+)', text)
        if not price:
            continue

        jan = re.findall(r'[0-9]{13}', text)

        item_data['name'] = text.split('JAN')[0].split('￥')[0]
        item_data['price'] = price[0]
        item_data['jan'] = jan[0] if jan else None

        print(item_data)
