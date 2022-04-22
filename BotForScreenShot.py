import logging 
import re
import asyncio
import bot_token as token
import requests
import urllib.parse
import os
import token

from PIL import Image
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage



#Logging level
logging.basicConfig(level=logging.INFO)

#Initalization of bot 
bot = Bot(token=token.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["status"])
async def status(message: types.Message):
	await message.reply("I'am still working my Lord")

@dp.message_handler(commands=["make_screenshot"])
async def makeing_screenshot(message: types.Message):
    get_data('http://www.gps110.org/user/index.aspx?father_id=d7c743a5-6928-4738-8904-fbdaa08e6786&login_id=d7c743a5-6928-4738-8904-fbdaa08e6786&isDealer=false&r=1650527444529&logOut=&mds=28a1f34fa6764123a9ed16ebd17f8316')
    opened_image = open("target1.jpg", "rb")
    await bot.send_photo(message.from_user.id, opened_image)

@dp.message_handler(commands=["timeline"])
async def nowing_timeline(message: types.Message):

    await bot.send_message(message.from_user.id, ("start %d, end %d, interval %d" % (start_time, end_time, interval/60)))

#setting's for screenshot making time
start_time = 21
end_time = 2
interval = 3600

class Mydialog(StatesGroup):
    otvet = State()  # Will be represented in storage as 'Mydialog:otvet'

#Здесь мы начинаем общение с клиентом и включаем состояния
@dp.message_handler(commands=["make_custom_timline"])
async def cmd_dialog(message: types.Message):
    await Mydialog.otvet.set()  # вот мы указали начало работы состояний (states)

    await message.reply("Ok send me your settings in this format \n Satrt at 21 hour end at 7 hour with interval 60 minuets (pleace write interval use a minuets)")

# А здесь получаем ответ, указывая состояние и передавая сообщение пользователя
@dp.message_handler(state=Mydialog.otvet)
async def process_message(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        
        try:
            parser = r"(?P<start>\d+)\s\w+"
            result = re.findall(parser, user_message)
            global start_time
            global end_time
            global interval
            start_time = int(result[0])
            end_time = int(result[1])
            interval = int(result[2]) * 60
        
        except Exception as e:
            await bot.send_message(message.from_user.id, "time line dosen't change", parse_mode='HTML')
        
        answer_for_user = ("Ok I'll start at %d hour end at %d hour with interval %d minuets" % (start_time, end_time, interval/60))
        
        await bot.send_message(message.from_user.id, answer_for_user , parse_mode='HTML')
        

    # Finish conversation
    await state.finish()  # закончили работать с сотояниями


async def makeing_screenshot_for_night():
    
    while True:
        date = datetime.now()
        try:
            await asyncio.sleep(1)
            if int(date.hour) >= start_time or int(date.hour) <= end_time: 
                get_data('http://www.gps110.org/user/index.aspx?father_id=d7c743a5-6928-4738-8904-fbdaa08e6786&login_id=d7c743a5-6928-4738-8904-fbdaa08e6786&isDealer=false&r=1650527444529&logOut=&mds=28a1f34fa6764123a9ed16ebd17f8316')           
                opened_image = open("target1.jpg", "rb")

                await bot.send_photo(token.chat_id_my, opened_image)
                await bot.send_message(token.chat_id_my, "photo sended")
                await bot.send_photo(token.chat_id_my, opened_image)

                await asyncio.sleep(interval)
        except asyncio.TimeoutError:
            await bot.send_message(token.chat_id_my, "error happends")

def get_image_from_web(url: str) -> None:
    BASE = 'https://mini.s-shot.ru/4096x2160/JPEG/4096/Z100/?'
    url = urllib.parse.quote_plus(url)
    path = 'target1.jpg'
    response = requests.get(BASE + url, stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response:
                file.write(chunk)

def get_data_from_image(image_path: str) -> dict:
    image = Image.open(image_path)
    image = image.crop((0, 265, 400, 460))
    image.save('target1.jpg')

def get_data(url: str):
    if os.path.exists('target1.jpg'):
        os.remove('target1.jpg')
        print('we here')
    get_image_from_web(url)
    get_data_from_image('target1.jpg')
           
async def on_startup(_):
    asyncio.create_task(makeing_screenshot_for_night())

#Runing code
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup = on_startup)
