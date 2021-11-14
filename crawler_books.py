import json
import sys
import requests
from bs4 import BeautifulSoup
import urllib.request as r
import urllib.parse as up
import pandas as pd



def getData(num_searched, item_searched, results):
    PAGE = 100
    error_tol = 3
    errorNum = 0
    for pageNum in range(PAGE):
        url = f'https://search.books.com.tw/search/query/key/{item_searched}/cat/all/page/{pageNum+1}'
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }

        try:
            res = requests.get(url, headers=header)
            root = BeautifulSoup(res.text, 'lxml')
            item_list = root.select('#itemlist_table')
            items = item_list[0].find_all('tbody')
            item_list = []
            for item in items:
                book_info = (item.find_all('div', class_='box_1'))[0]
                book_title = book_info.a.get('title')
                book_url = 'https:' + book_info.a.get('href')
                book_publish_info = (item.find_all('ul', class_='list-date clearfix'))[0]
                book_publish = book_publish_info.li.find_all('a')[-1].text
                book_price_info = (item.find_all('ul', class_='list-nav clearfix'))[0]
                book_price = book_price_info.li.text
                item_list.append((book_title, [book_price, book_publish, book_url]))
                num_searched -= 1
                if num_searched == 0:
                    break
            results = results + item_list
            res.close()
        except ConnectionError as exc:
            errorNum += 1
            print(exc)
            pass
        except:
            if errorNum == error_tol:
                results = []
                results.append((('網路連線有異常，或是查無符合項目，請稍後再嘗試！'), ['', '', '']))
                return results
            else:
                errorNum += 1
                print('有錯誤')
                pass
        if num_searched == 0:
            break
    return results

