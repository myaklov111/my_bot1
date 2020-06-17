from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command,Text
from aiogram.types import Message,ReplyKeyboardRemove
import aiohttp
import keyboards
from status import TEST
import config
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import func
import sqlite as sql
import time
import asyncio
import Avito_Parser


proxy='socks5://aWdrxQ:YGppgp@108.187.204.26:8000'

PROXY_URL ='http://104.227.97.168:8000'

STOP=True


PROXY_AUTH = aiohttp.BasicAuth(login='qY5bWs', password='kjMHoV')

FIRST_POST={'title':'','url':'','price':'','img':''}

storage = MemoryStorage()
bot = Bot(token=config.API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)

#bot = Bot(token=config.API_TOKEN)

dp = Dispatcher(bot,storage=storage)





async def replace_link(link:str):
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


async def write_link(message: types.Message,state:FSMContext):
    global STOP
    global proxy
    if message.text == 'Назад':
        await state.finish()
        await message.reply(config.WELCOM_TEXT, reply_markup=keyboards.main_menu)
    else:
        link_tp=str(message.text).strip()
        link=await replace_link(link_tp)

        parser=Avito_Parser.Avito_Parser(link,proxy,0)
        base=parser.parsing()

        if base!=None and len(base)>0:
            tstap=int(base[0])

            async with state.proxy() as data:
                data['Q1'] = link
            try:
                flag=False
                if sql.select_users_check_user_time(message.chat.id):
                    if sql.update_user_link(message.chat.id,link,tstap):
                        flag=True
                        STOP=True

                else:
                    if sql.add_users_user(message.chat.id,link,0,24,tstap):
                        flag = True
                if flag==True:
                    await message.reply(config.WRITE_LINK_TEXT, reply_markup=keyboards.main_menu)
                    await state.finish()
                else:
                    await message.reply(config.BAD_ADD_LINK, reply_markup=keyboards.back_menu)
            except:
                await message.reply(config.BAD_ADD_LINK, reply_markup=keyboards.back_menu)

        else:
            print('неправильная ссылка')
            await message.reply(config.BAD_LINK_TEXT, reply_markup=keyboards.back_menu)

async def write_time(message: types.Message,state:FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await message.reply(config.WELCOM_TEXT, reply_markup=keyboards.main_menu)
    else:
        kt=func.check_time(message.text)
        if kt!=None:

            async with state.proxy() as data:
                data['Q2'] = str(message.text).strip()
                if sql.update_user_time(message.chat.id,kt[0],kt[1]):

                    await message.reply(config.WRITE_TIME_TEXT, reply_markup=keyboards.main_menu)
                    await state.finish()
                else:
                    await message.reply(config.BAD_WRITE_TIME_TEXT, reply_markup=keyboards.back_menu)

        else:
            print('неправильное время')
            await message.reply(config.BAD_WRITE_TIME_TEXT, reply_markup=keyboards.back_menu)




async  def send_welcom(message: types.Message):
    markup=keyboards.main_menu
    if message.chat.id==config.ADMIN_ID:
        markup=keyboards.main_menu_admin

    await message.reply(config.WELCOM_TEXT, reply_markup=markup)

async  def send_back_welcom(message: types.Message):
    markup = keyboards.main_menu
    if message.chat.id == config.ADMIN_ID:
        markup = keyboards.main_menu_admin
    await message.reply(config.BACK_TEXT, reply_markup=markup)


async  def send_help(message: types.Message):
   await message.reply(config.HELP_TEXT, reply_markup=keyboards.main_menu)


async  def send_settings(message: types.Message):
    await message.reply(config.SETTINGS_TEXT, reply_markup=keyboards.settings_menu)

async  def send_add_link(message: types.Message):
    await message.reply(config.ADD_LINK_TEXT, reply_markup=keyboards.back_menu)
    await TEST.Q1.set()

async  def send_set_time(message: types.Message):
    await message.reply(config.ADD_TIME_TEXT, reply_markup=keyboards.set_time_menu)

async  def send_set_time_2(message: types.Message,state=None):
    await message.reply(config.SET_TIME_TEXT, reply_markup=keyboards.back_menu)
    await TEST.Q2.set()






@dp.message_handler(state=TEST.Q2)
async def answer_time(message:types.Message,state:FSMContext):
    answer=message.text
    await write_time(message,state)


@dp.message_handler(state=TEST.Q1)
async def answer_link(message:types.Message,state:FSMContext):
    answer=message.text
    await  write_link(message,state)






@dp.message_handler(Command("help"),state=None)
async def send_welcome(message: types.Message):
    await send_help(message)

@dp.message_handler(Text(equals=["Назад"]))
async def send_back_text(message: types.Message):
    await send_back_welcom(message)

@dp.message_handler(Text(equals=["Помощь"]))
async def send_help_text(message: types.Message):
    await send_help(message)

@dp.message_handler(Text(equals=["Настройки"]))
async def send_settings_text(message: types.Message):
    await send_settings(message)



@dp.message_handler(Text(equals=["Добавить ссылку"]))
async def send_add_link_text(message: types.Message):
    await send_add_link(message)

@dp.message_handler(Text(equals=["Настройка времени"]))
async def send_set_time_text(message: types.Message):
    await send_set_time(message)

@dp.message_handler(Text(equals=["Установить время"]))
async def send_set_time_text_2(message: types.Message):
    await send_set_time_2(message)



@dp.message_handler(Text(equals=["Управление"]))
async def send_conntrol_menu(message: types.Message):
    try:
        res = sql.select_users_user_all(message.chat.id)
        print(res)
        if res != None:
            vk = 'Мониторин выключен'
            if res[6] == 1:
                vk = 'Мониторинг включен'
            st = vk + '\nВаши настройки:\nВремя: от ' + str(res[3]) + ' до ' + str(res[4]) + '\n' + 'Ссылка: ' + str(
                res[2]) + '\n\n'

            await message.reply(st, reply_markup=keyboards.main_menu_control)
        else:
            await send_welcom(message)
    except:
        await send_welcom(message)
    #await message.reply(config.CONTOL_MONITOR_TEXT, reply_markup=keyboards.main_menu_control)






@dp.message_handler(Text(equals=["Старт"]))
async def start_monitor(message: types.Message):
    global STOP
    STOP=False
    try:
        res=sql.select_users_user_all(message.chat.id)
        if res!=None:
            vk='Мониторин выключен'
            if str(res[2])!='':
                if sql.update_vk(message.chat.id,1):
                    await message.reply(config.START_MONITOR_TEXT, reply_markup=keyboards.main_menu)


            else:
                await message.reply(config.NO_LINK_TEXT, reply_markup=keyboards.main_menu)
        else:
            await message.reply(config.NO_LINK_TEXT, reply_markup=keyboards.main_menu)

    except:
        pass




@dp.message_handler(Text(equals=["Стоп"]))
async def stop_monitor(message: types.Message):
    global STOP
    STOP=True
    try:
        res = sql.select_users_user_all(message.chat.id)
        if res != None:
            vk = 'Мониторин включен'
            if str(res[2]) != '':
                if sql.update_vk(message.chat.id, 0):
                    await message.reply(config.STOP_MONITOR_TEXT, reply_markup=keyboards.main_menu)

            else:
                await message.reply(config.NO_LINK_TEXT, reply_markup=keyboards.main_menu)

    except:
        pass








@dp.message_handler(Command("start"),state=None)
async def send_welcome_text(message: types.Message):
    global STOP
    STOP = False
    try:
        res=sql.select_users_user_all(message.chat.id)
        print(res)
        if res!=None:
            vk='Мониторин выключен'
            if res[6]==1:
                vk='Мониторинг включен'
            st=vk+'\nВаши настройки:\nВремя: от '+str(res[3])+' до '+str(res[4])+'\n'+'Ссылка: '+str(res[2])+'\n\n'

            await message.reply(st, reply_markup=keyboards.main_menu)
        else:
            await send_welcom(message)
    except:
        await send_welcom(message)


@dp.message_handler(Text(equals=["Админ_панель"]))
async def view_admin_panel(message: types.Message):
    if message.chat.id == config.ADMIN_ID:
        try:
            await bot.send_message(message.chat.id,'админ панель',reply_markup=keyboards.menu_admin)
        except:
            print('ошибка бота')



@dp.message_handler(Text(equals=["Статистика"]))
async def get_static_users(message: types.Message):
    if message.chat.id==config.ADMIN_ID:
        try:
            data=sql.select_all_users()
            if data!=None:
                count= str(len(data))
                s="\n"
                for m in data:
                    s=s + str(m[1])+'\n'


                try:
                    await bot.send_message(message.chat.id, f'в базе записано {count} пользователей {s}', reply_markup=keyboards.menu_admin)
                except:
                    print('ошибка бота')

        except:
            print('ошибка выборки статистики')

















async def page_parsing(link:str,proxy:str,last_pars:int):
    try:
        parser=Avito_Parser.Avito_Parser(link,proxy,last_pars)
        data = parser.parsing()
        if data!= None:
            return data
        else:
            return None
    except:
        return None


async def tg_posting(chat_id:int,base):
        for cap in base:
            try:
                time.sleep(1)
                if cap['url']!='' and cap['img']!='' and cap['title']!='' and cap['price']!='':
                    sent = '<a href="{}">{}</a> \n\nцена: {}'.format(cap['url'],cap['title'],cap['price'])
                    try:
                        await bot.send_photo(chat_id,cap['img'],sent,parse_mode='HTML')
                        print('отправили пост')
                    except:
                        print('ошибка отправки поста')
                        continue

            except:
                continue




async def start_parser():
    global proxy
    try:
        print('проверка заданий в базе')
        res = sql.select_users_for_pars()
        if res != None:
            for mas in res:
                try:
                    print('выполняем задания')
                    link = mas[2]
                    last_pars = mas[5]
                    if last_pars==None:
                        last_pars=0
                    chat_id = mas[1]

                    data = await page_parsing(link,proxy,last_pars)
                    if data!=None:
                        last_pars=int(data[0])
                        base =data[1]
                        count=len(base)
                        print('обновляем запись last_pars в базе')
                        sql.update_last_pars(chat_id, last_pars)
                        print(f'отправляем посты в телеграм: всего {count} постов')
                        await tg_posting(chat_id,base)


                    else:
                        print('база для парсинга пустая')



                except:
                    continue
    except:
        return None


async def parsing(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        await start_parser()









if __name__ == '__main__':

    dp.loop.create_task(parsing(config.TIME_PARSING))
    executor.start_polling(dp, skip_updates=True)


