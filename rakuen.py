import re
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    lite_color = {
        '4902370542929': 'グレー',
        '4902370542943': 'ターコイズ',
        '4902370542936': 'イエロー',
        '4902370545302': 'コーラル'
    }

    url = "http://keitairakuen.com/category/household/game/nintendo/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    li_list = soup.find_all('li', attrs={'class': 'article'})

    item_list = list()
    for li in li_list:
        # タグ取得
        h3_tag = li.find('h3', attrs={'class': 'title'})
        if not h3_tag:
            continue

        # 商品名取得
        h3_tag_contents = h3_tag.contents
        if not h3_tag_contents:
            continue

        name = h3_tag_contents[0].strip()
        if 'jan' in name:
            name = name.split('jan')[0]

        if 'JAN' in name:
            name = name.split('JAN')[0]

        # JANコードリスト取得
        jan_list = re.findall(r'[0-9]{13}', h3_tag.text)

        # 買取価格リストを取得
        p_tag = li.find('p')
        if not p_tag:
            continue

        price_list = re.findall(r'([0-9]+)円', p_tag.text.replace(',', ''))

        # JANコードリストと買取価格リストの長さが同一なら追加
        if not (len(jan_list) == len(price_list)):
            continue

        for jan, price in zip(jan_list, price_list):
            # 入れ物
            item_data = dict()

            # 色のバリデーション
            if jan in lite_color:
                item_data['name'] = f'{name} {lite_color[jan]}'
            else:
                item_data['name'] = name
            item_data['jan'] = jan
            item_data['price'] = price

            print(item_data)
            item_list.append(item_data)
