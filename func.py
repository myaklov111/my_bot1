from datetime import date, timedelta
import datetime as DT

FIRST_PAGES_ID="1980-10-01 10:10:10"

FIRST_POST={'title':'','url':'','price':'','img':''}

DATE_DICT={'января':'01','февраля':'02','марта':'03','апреля':'04','мая':'05','июня':'06','июля':'07','августа':'08','сентября':'09','октября':'10','ноября':'11','декабря':'12'}

proxy='socks5://aWdrxQ:YGppgp@108.187.204.26:8000'


def replace_link(link:str):
    st=link
    if link.startswith('https://m.avito.ru'):
        st=link.replace('https://m.avito.ru','https://www.avito.ru')
    elif link.startswith('http://m.avito.ru'):
        st=link.replace('http://m.avito.ru','https://www.avito.ru')
    elif link.startswith('m.avito.ru'):
        st=link.replace('m.avito.ru','https://www.avito.ru')
    elif link.startswith('www.avito.ru'):
        st=link.replace('www.avito.ru','https://www.avito.ru')
    return st




def date_plus(day:int):
    today = date.today()
    days = timedelta(day)
    new_date = today + days
    return new_date

def check_date(end_date):
    today = date.today()
    d=DT.datetime.strptime(end_date,'%Y-%m-%d').date()
    if today<=d:

        return True
    else:
        return False









def check_link_update(link):
    global FIRST_PAGES_ID
    global FIRST_POST


    FIRST_PAGES_ID = "1900-10-01 10:10:10"

    dt_fmt = '%Y-%m-%d %H:%M'
    f_date = DT.datetime.strptime(FIRST_PAGES_ID,dt_fmt)
    base_id_items = set()

    st=replace_link(link)
    print(st)

    s='https://www.avito.ru'
    if st.startswith(s):
        try:
            link=st

            base = get_link(link)
            if base != None:
                b_items = soup_parsing(base,base_id_items)[0]
                if b_items != None:
                    if len(b_items) >0:
                        for m in b_items:
                            try:
                                date1=str_to_date(m['time'])
                                if date1>f_date:
                                    f_date=date1
                                    FIRST_PAGES_ID=str(f_date)
                                    FIRST_POST['title']=m['title']
                                    FIRST_POST['url'] = m['url']
                                    FIRST_POST['price'] = m['price']
                                    FIRST_POST['img'] = m['img']

                            except:
                                continue
                        return True
                else:
                    return False
        except:
            return False
    return False








def check_link(link:str,proxy:str,last_pars:int):
    pass



def check_time(time_data:str):
    try:
        m=time_data.split('-')
        x=int(m[0])
        y=int(m[1])
        if x>-1 and x<25 and y>-1 and y<25 and x<y:
            return (x,y)
        else:
            return None
    except:
        return None

