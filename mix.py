import re
import requests
from bs4 import BeautifulSoup


def mix():
    url = "http://mobile-mix.jp/apple.php"
    response = requests.get(url)

    if response.status_code != 200:
        return

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'list desktop'})

    if not table:
        return

    tr_list = table.find_all('tr')

    if not tr_list:
        return

    data_list = list()
    for tr in tr_list:
        td_list = tr.find_all('td')
        if not td_list:
            continue

        model_tag = td_list[0].contents[1]
        model = model_tag.text if type(model_tag).__name__ == 'Tag' else str(model_tag)

        nb = td_list[1].text
        price_text = re.sub(r'[^0-9]+', '', td_list[2].text) if td_list[2].text else ''
        price = int(price_text) if price_text else 0

        data = dict()
        data['model'] = model
        data['price'] = price
        data['nb'] = nb
        data_list.append(data)

    return {'shop': 'mix', 'data': data_list}


if __name__ == '__main__':
    import json
    j = mix()
    print(json.dumps(j, ensure_ascii=False, indent=2))
