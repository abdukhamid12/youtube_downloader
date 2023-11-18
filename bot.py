import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import *
from utils import *
import os
from btn import *
from states import *


BOT_TOKEN = "6600379465:AAEf5a5cCTMtJ3HSj1L8Msd94UdK-w1fEoY"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

ADMINS = [1037348868]


async def command_menu(dp: Dispatcher):
  await dp.bot.set_my_commands(
    [
      types.BotCommand('start', 'Ishga tushirish'),
    ]
  )
  await create_tables()
  # nega command menudan keyin chaqirvommiz chunki start_pulling qiganimizda command menu bir marta ishga tushadi va oshanda birmatta create_tables ham ishga tushadi


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
  await add_user(message.from_user.id)
  await message.answer("Welcome to the youtube dowloader bot !")

@dp.message_handler(commands=['admin'])
async def totals_user(message: types.Message):
  if message.from_user.id in ADMINS:
    score = await total_user()
    await message.answer(f"botni ishlatgan odamlar soni: {score}", reply_markup=menu)



@dp.message_handler(commands=['send'])
async def send_handler(message: types.Message):

  if message.from_user.id in ADMINS:
    await message.answer("Xabarni yuboring:")

    await AdminStates.mailing.set()


@dp.message_handler(content_types=['text', 'photo', 'video', 'audio', 'animation', 'voice'], state=AdminStates.mailing)
async def mailing_state(message: types.Message, state: FSMContext):
  text = message.text
  content = message.content_type

  users = await get_all_users_id()

  await state.finish()

  for user in users:
    if content == 'text':
      await bot.send_message(chat_id=user[0], text=text)
    elif content == 'photo':
      await bot.send_photo(chat_id=user[0], photo=message.photo[-1].file_id)
    elif content == 'video':
      await bot.send_video(chat_id=user[0], video=message.video.file_id)
    elif content == 'animation':
      await bot.send_animation(chat_id=user[0], animation=message.animation.file_id)
    elif content == 'audio':
      await bot.send_audio(chat_id=user[0], audio=message.audio.file_id)
    elif content == 'voice':
      await bot.send_voice(chat_id=user[0], voice=message.voice.file_id)

@dp.message_handler(content_types=["text"])
async def text_handler(message: types.Message):
  text = message.text

  if text .startswith("https://youtube.com") or text.startswith("https://youtu.be"):
    wait_msg = await message.answer("⏳")
    video = await download_video_by_url(text, message.from_user.id)

    await wait_msg.delete()
    if video == 1:
      await message.answer("Video tortishda hatolik!")
    elif video:
      await message.answer_video(types.InputFile(video))
      os.remove(video)
    else:
      await message.answer("Video 50 mb dan kotta")


if __name__ == "__main__":
  executor.start_polling(dp, on_startup=command_menu)