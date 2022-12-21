# to delete files
import glob
import logging

# System libraries
import os
from dotenv import load_dotenv
# time
from datetime import datetime
from qreader import QReader
import cv2

# from kraken import binarization
# from PIL import Image

# QR Code
# from pyzbar.pyzbar import ZBarSymbol, decode

# Telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PollAnswerHandler,
    filters,
)
load_dotenv()
TOKEN = os.getenv("TOKEN")


def decode_image(file_name: str) -> str:
    qreader = QReader()
    image = cv2.imread(file_name)
    # изначально использовал только pyzbar но он плохо обрабатывает изображения с телефона
    # на stackoverwlow нашел этот пост
    # https://stackoverflow.com/questions/61442775/preprocessing-images-for-qr-detection-in-python/61443430#61443430
    # по этому подключил kraken в нем есть nlbin он выполняет бинаризацию с использованием нелинейной обработки
    # так же нашел либу 
    # bw_im = binarization.nlbin(im)
    # result = decode(bw_im, symbols=[ZBarSymbol.QRCODE])
    decoded_text = qreader.detect_and_decode(image)
    if decoded_text:
        print(decoded_text)
        return decoded_text


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Для старта бота нажмите /start, либо в левом нижнем углу выберите пункт меню")


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, help))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()