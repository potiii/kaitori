import re
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://www.kadenkaitori-co.jp/category/game.php'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')

    # 買取価格表の行を取得
    tr_list = soup.find('div', attrs={'id': 'details_right_table_01'}).find_all('tr')

    for tr in tr_list:
        item_data = dict()
        td_list = tr.find_all('td')

        # "行"がなければ次へ
        if not td_list:
            continue

        item_data['name'] = td_list[0].text.strip()
        item_data['price'] = int(re.sub(r'[^0-9]', '', td_list[1].text.strip()))
        item_data['nb'] = ' '.join([nb for nb in td_list[2].text.replace('\n', '').strip().split(' ') if nb])
        print(item_data)
