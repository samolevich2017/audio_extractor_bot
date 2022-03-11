from ast import parse
from email import message
from email.mime import audio
from encodings import utf_8
import logging
from operator import length_hint
from pyexpat.errors import messages
from sre_constants import ANY
from statistics import mode

from telegram import ParseMode
import classes.config as config
from aiogram import Bot, Dispatcher, executor, types
from classes import yt_extractor as yt
from classes.sqlighter import SQLighter
import os
import asyncio

from utils.extfunctions import message_from_file

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initializing Bot and Dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# Initializing connection with database
db = SQLighter('data/data_base.db')

# Function wich will be check - user already exists in db or not 
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
    await message.answer("Привет, " + str(message.from_user.first_name) + " 😉\n")
    # send message 2
    await message.answer("Меня зовут Минори 😊\nМоя работа заключается в том, что я буду конвертировать любые видео с YouTube в аудио формат. 🎧")
    # send message 3
    await message.answer("Просто кинь мне ссылку на видео, а я тебе верну его аудио 😇") 

# Command - get information about last update 
@dp.message_handler(commands=['updates'])
async def send_update_info(message: types.Message):
    # read the message about last updates from txt file
    content = message_from_file("last_upd.txt")
    await bot.send_message(message.from_user.id, content, parse_mode='Markdown')

# Function for /help command
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    content = message_from_file("help.txt")
    await bot.send_message(message.from_user.id, content, parse_mode='Markdown')

# Function listener - listen to all messages and process these
@dp.message_handler()
async def link_listener(message: types.Message):
    try:
        # if we need works with YouTube video
        if('https://www.youtube.com/' in message.text or 'https://youtu.be/' in message.text):

            # getting a link from the message
            url = message.text 

            # initializing object for YouTube extractor
            yt_ext = yt.YT_Extractor(url)
           
            # we ask awaiting for one second
            await message.answer("Одну секунду 😋")
            
            # extract audio from video and get the path to mp3 file
            audio_path = yt_ext.extract() 
            
            # send the audio to the user and then remove it
            await message.answer_audio(audio=open(audio_path, "rb"), title=yt_ext.get_track_title(), duration=yt_ext.get_duration())
            os.remove(audio_path)
        else:
            # if this message from the developer and he want to send a message about the update
            # send his message to all users in the database
            if(str(message.from_user.id) == "955228125" and message.text.__contains__("/new_update")):
                # write the message to the txt file about last updates
                with open("last_upd.txt", "w", encoding='UTF-8') as file:
                    file.write(message.text.replace("/new_update", ""))

                # send the message to all users
                for user in db.get_users():
                    await bot.send_message(user[1], message.text.replace("/new_update", ""), parse_mode='Markdown')
                return
            
            await message.answer("Что-то не то ты мне кидаешь 😕")
            await message.answer("Я понимаю только ссылки YouTube 😇")

    except Exception as ex:
        print(ex)
        await message.answer("Прости, но что-то пошло не так... 😞")
        await message.answer(f"Сообщи пожалуйста об этом моему разработчику 👇 \n{config.BOT_OWNER}")

# Command - will be answering when the user will be sending something except text
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def incorrect_message(message: types.Message):
    await message.reply("Я не знаю, что с этим делать 😐\nЯ просто напомню, что есть команда /help", parse_mode='Markdown')




# start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

