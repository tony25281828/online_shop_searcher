import json
import sys

import requests
from bs4 import BeautifulSoup


def getData(num_searched, item_searched, lower_limit, upper_limit, results):
    PAGE = 100
    errorNum = 0
    error_tol = 3
    if lower_limit == '':
        lower_limit = 0
    if upper_limit == '':
        upper_limit = sys.maxsize

    for pageNum in range(PAGE):
        url = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={item_searched}&page={pageNum + 1}&sort=sale/dc&price={int(lower_limit)}-{int(upper_limit)}'
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        try:
            res = requests.get(url, headers=header)
            data = json.loads(res.text)
            items = data['prods']
            item_list = []
            for item in items:
                item_id = item['Id']
                item_url = f'https://24h.pchome.com.tw/prod/{item_id}'
                item_name = item['name']
                item_price = item['price']
                item_list.append((item_name, [item_price, item_url]))
                num_searched -= 1
                if num_searched == 0:
                    break
            results = results + item_list
            res.close()
        except:
            if errorNum == error_tol:
                results = []
                results.append((('網路連線有異常，或是查無符合項目，請稍後再嘗試！'), ['', '']))
                return results
            else:
                errorNum += 1
                print('有錯誤')
                pass
        if num_searched == 0:
            break
    return results



