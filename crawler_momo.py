import sys
from bs4 import BeautifulSoup
import requests


def getData(num_searched, item_searched, lower_limit, upper_limit, results):
    PAGE = 100
    errorNum = 0
    error_tol = 3
    for pageNum in range(PAGE):
        url = f'https://m.momoshop.com.tw/search.momo?searchKeyword={item_searched}&curPage={pageNum+1}&searchType=1&cateLevel=2&ent=k&_advPriceS={lower_limit}&_advPriceE={upper_limit}'
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        try:
            res = requests.get(url, headers=header)
            root = BeautifulSoup(res.text, 'lxml')
            data = root.find_all('li', class_='goodsItemLi')
            item_list = []
            for item in data:
                item_id = item.a.find('input').get('value')
                item_url = f'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code={item_id}'
                item_name = item.a.get('title')
                item_price = item.find('b', class_='price').text
                item_list.append((item_name, [item_price, item_url]))
                num_searched -= 1
                if num_searched == 0:
                    break
            results = results + item_list
            res.close()
            if len(results) == 0:
                results.append((('無符合項目或找無此商品！'), ['', '']))
                return results
        except:
            if errorNum == error_tol:
                results = []
                results.append((('網路連線有異常，請稍後再嘗試！'), ['', '']))
                return results
            else:
                errorNum += 1
                print('有錯誤')
                pass
        if num_searched == 0:
            break
    return results


