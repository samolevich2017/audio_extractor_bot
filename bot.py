from email import message
import logging
from pyexpat.errors import messages
import config
from aiogram import Bot, Dispatcher, executor, types
from classes import yt_extractor as yt
from sqlighter import SQLighter
import os

# configure logging
logging.basicConfig(level=logging.INFO)

# init Bot and Dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# initializing connection with database
db = SQLighter('data/data_base.db')

# initializing object for YouTube extractor
yt_ext = yt.YT_Extractor()

# function wich will be check - user already exists in db or not 
# and switch subscription status 
def isSubscribe(message):
    if(not db.user_exists(message.from_user.id)):
        # if user is not exists in db, adding him with subscription status ON
        db.add_user(message.from_user.id, message.from_user.full_name, True)
    else:
        # if user already exists in db, update his subscription status 
        db.update_subscribe(message.from_user.id, True)


# Welcome command which will be adding user if him is a new
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # process checking subscribe
    isSubscribe(message)

    # send message 1
    await message.answer("Привет, " + str(message.from_user.first_name) + " 😉\nКак меня зовут, я пока не скажу, потому что мой господин не придумал мне имени. 🥺")
    # send message 2
    await message.answer("Моя работа заключается в том, что я буду конвертировать любые видео с YouTube в аудио формат. 🎧")
    # send message 3
    await message.answer("Просто кинь мне ссылку на видео с YouTube, а я тебе верну его аудио 😇") 


# Function listener - listen to all messages and process these
@dp.message_handler()
async def link_listener(message: types.Message):
    try:
        # if we need works with YouTube video
        if('https://www.youtube.com/' in message.text or 'https://youtu.be/' in message.text):
           
            # we ask awaiting for one second
            await message.answer("Одну секунду 😋")
            
            # getting a link from the message
            url = message.text 
            
            # extract audio from video and get the path to mp3 file
            audio_path = yt_ext.extract(url) 
            
            # send the audio to the user and then remove it
            await message.answer_audio(audio=open(audio_path, "rb"))
            os.remove(audio_path)
        else:
            await message.answer("Что-то не то ты мне кидаешь 😕")
            await message.answer("Я понимаю только ссылки YouTube 😇")
        
    except Exception as ex:
        print(ex)
        await message.answer("Прости, но что-то пошло не так... 😞")
        await message.answer(f"Сообщи пожалуйста об этом моему разработчику 👇 \n{config.BOT_OWNER}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

