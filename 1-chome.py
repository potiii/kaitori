import re
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # url = "https://www.1-chome.com/elec"
    url = "https://www.1-chome.com/elec/cate/20050031/Nintendo%20%20%E3%82%B2%E3%83%BC%E3%83%A0%E6%A9%9F"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div_list = soup.find_all('div', attrs={'class': 'col-sm-4 col-xs-4'})

    item_list = list()
    for div in div_list:
        # 入れ物
        item_data = dict()

        # 価格の取得
        price_element = div.find('span', attrs={'class': 'text-danger'})
        price = price_element.text if price_element else None
        price = int(re.sub(r'[^0-9]', '', price)) if price else None
        item_data['price'] = price

        # 名前と備考の取得
        content = div.find('h6', attrs={'class': 'h6 g-mb-5 text-left g-font-size-13'})
        content = content.text if content else None
        content = [value.strip() for value in content.split('\n') if value] if content else None
        item_data['name'] = content[1] if content else None
        item_data['nb'] = content[2] if content else None

        # JANの取得
        jan_element = div.find('h6', attrs={'class': 'g-font-size-12 g-mb-0'})
        jan_text = jan_element.text if jan_element else None
        jan_code = re.sub(r'[^0-9]', '', jan_text) if jan_text else None
        item_data['jan'] = jan_code

        item_list.append(item_data)

        print(item_data)








