import datetime as DT
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs


class Avito_Parser:
    link=''
    proxy=''
    last_pars=0

    def __init__(self,link:str,proxy:str,last_pars:int):
        self.link=link
        self.proxy=proxy
        self.last_pars=last_pars

    def get_link(self):
        try:

            ua = UserAgent()
            agent = ua.random
            headers = {
                'User-Agent': agent,
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'Upgrade-Insecure-Requests': '1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive'
            }

            get_html = requests.get(self.link,
                                    proxies=dict(http=self.proxy,
                                                 https=self.proxy), headers=headers)

            soup = bs(get_html.text, 'html.parser')
            base = soup.findAll('div', class_='snippet-horizontal')
            if len(base) > 0:
                return base
            else:
                return None
        except:
            return None

    def parse_date(self,item: str):
        DATE_DICT = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                     'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

        dt_fmt = '%d.%m.%Y %H:%M:%S'
        try:
            now = DT.datetime.now()
            year = now.year
            params = item.strip().split(' ')
            if len(params) == 3:
                params[1] = DATE_DICT[params[1]]
                vr = f'{params[0]}.{params[1]}.{year} {params[2]}:00'
                d = DT.datetime.strptime(vr, dt_fmt).timestamp()
                return d
            else:
                return None
        except:
            return None

    def soup_parsing(self,base):
        base_result = []
        last = 0
        for b in base:
            item = {}
            try:

                g_link = b.find('a', class_='snippet-link')['href']
                g_title = b.find('a', class_='snippet-link')['title']
                g_price = b.find('span', class_='snippet-price').text

                g_img = b.find('img', class_='large-picture-img')['src']

                g_item_id = b['data-item-id']

                g_time1 = b.find('div', class_='snippet-date-info')['data-tooltip']

                g_time =self.parse_date(g_time1)

                if g_time > self.last_pars:
                    if g_time > last:
                        last = g_time

                    item['id'] = g_item_id
                    item['url'] = 'https://www.avito.ru' + g_link
                    item['img'] = g_img
                    item['title'] = g_title
                    item['price'] = g_price
                    item['time'] = g_time

                    base_result.append(item)
                else:
                    print('старая запись')




            except:
                continue

        if len(base_result) > 0:
            return [last, base_result]
        else:
            return None


    def parsing(self):
        try:
            base=self.get_link()
            if base!=None:
                items=self.soup_parsing(base)
                if items!=None:
                    return items
                else:
                    return None
            else:
                return None
        except:
            return None
