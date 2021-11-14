import sys

import requests
from bs4 import BeautifulSoup




def getData(num_searched, item_searched, lower_limit, upper_limit, results):
    PAGE = 100
    error_tol = 3
    errorNum = 0
    for pageNum in range(PAGE):
        url = f'https://tw.buy.yahoo.com/search/product?p={item_searched}&pg={pageNum+1}'
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }

        try:
            res = requests.get(url, headers=header)
            root = BeautifulSoup(res.text, 'lxml')
            data = root.find('div', class_='ResultList_resultList_IpWJt')
            items = data.find_all('ul', class_='gridList')[0].find_all('li', class_='BaseGridItem__grid___2wuJ7 BaseGridItem__multipleImage___37M7b')
            item_list = []
            for item in items:
                item_price_info = item.select('.BaseGridItem__price___31jkj')[0].text.split('$')
                item_price = int(item_price_info[1].replace(',', ''))
                item_url = item.a.get('href')
                item_name = item.find('span', class_='BaseGridItem__title___2HWui').text
                if lower_limit == '' and upper_limit == '':
                    item_list.append((item_name, [item_price, item_url]))
                    num_searched -= 1
                elif lower_limit != '' and upper_limit != '':
                    if int(lower_limit) <= item_price <= int(upper_limit):
                        item_list.append((item_name, [item_price, item_url]))
                        num_searched -= 1
                elif lower_limit != '' and upper_limit == '':
                    if int(lower_limit) <= item_price:
                        item_list.append((item_name, [item_price, item_url]))
                        num_searched -= 1
                elif lower_limit == '' and upper_limit != '':
                    if item_price <= int(upper_limit):
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



