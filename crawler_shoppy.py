#抓取蝦皮的網路原始碼(HTML)

import urllib.request as req
import json
import urllib.parse as up
import sys



def getData(num_searched, item_searched, lower_limit, upper_limit, results):
    pageURL1 = "https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword="
    pageURL3 = "&limit=60&newest="
    pageURL4 = "&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    PAGE = 100
    errorNum = 0
    error_tol = 3

    for pageNum in range(PAGE):
        url = pageURL1 + item_searched + pageURL3 + str(pageNum * 60) + pageURL4
        # 建立一個request物件，附加headers資訊，讓自己看起來比較像人類
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        })

        try:
            with req.urlopen(request) as response:
                data = response.read().decode("utf-8")  # 根據觀察，取得的資料是JSON格式

            # 解析JSON資料，取得商品標題
            # 把原始的資料解析成字典或列表的形式
            data = json.loads(data)
            # print(data)
            # 取得JSON資料中的商品標題
            items = data["items"]
            # print(type(items))

            item_list = []
            for item in items:
                item_name = item['item_basic']['name']
                item_price = int(int(item['item_basic']['price']) / 100000)
                item_url = 'https://shopee.tw/' + up.quote(item['item_basic']['name']) + '-i.' + str(item['item_basic']['shopid']) + '.' + str(item['item_basic']['itemid']) + '?' + 'adsid=' + str(item['adsid'])+'&campaignid=' + str(item['campaignid'])
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




