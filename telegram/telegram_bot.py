# to delete files
import glob
# System libraries
import os
import logging
import cv2
from datetime import datetime

# QR Code
from qreader import QReader

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

# SQL request in to Database
from telegram_db import (
    check_id,
    detail_device,
    detail_employee,
    detail_office,
    detail_office_all,
    insert_inventory_card,
    movents,
    select,
    select_bio_employee,
    update_chat_id,
)

# Settings
from config import settings

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


CHOICES, COMPUTER, PEOPLE, OFFICE, NEXT_EMPLOYEE_OR_ROOM, POOL, NEXT, DETAIL, DETAIL_CHOICE, CONTACT = range(10)

# KEYBOARDS
REPLY_KEYBOARD = [["Учёт", "Сверка", "Перемещение", "Получить информацию", "Выход"]]
REPLY_KEYBOARD_NEXT = [["Следующий сотрудник", "Следующее помещение", "Меню", "Выход"]]
REPLY_KEYBOARD_YES_NOT = [["Да", "Нет"]]

NOW = datetime.now().strftime("%H:%M:%S")

EMPLOYEE_OFFICE_DEVICE = {
    "device": "устройства",
    "office": "офиса",
    "employee": "сотрудника"
    }

# bot token
TOKEN = settings.TOKEN


#  ------------------------------Decode function--------------------------------
def decode_image(file_name: str) -> str:
    qreader = QReader()
    image = cv2.imread(file_name)
    # изначально использовал только pyzbar но он плохо обрабатывает изображения с телефона
    # на stackoverwlow нашел этот пост
    # https://stackoverflow.com/questions/61442775/preprocessing-images-for-qr-detection-in-python/61443430#61443430
    # по этому подключил kraken в нем есть nlbin он выполняет бинаризацию с использованием нелинейной обработки
    # в дальнейшем нашел либу qreader
    decoded_text = qreader.detect_and_decode(image)
    if decoded_text:
        return decoded_text
# ------------------------------------------------------------------------------


# ------------------------------Delete image------------------------------------
def delete_all_image(user: str) -> None:
    for file in glob.glob(f"./static_telegram/{user}*.jpg"):
        os.remove(file)
# ------------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about function"""

    user_id = update.message.from_user.id
    result = await check_id(user_id)  # check if the id is in our database
    if result:
        await update.message.reply_text(
            "Добрый день, выберите нужную фунцию",
            reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD, one_time_keyboard=True),
        )
        return CHOICES
    await update.message.reply_text(
        "Отправьте ваш контакт. Нажмите на верхний правый угол, отправить свой контакт.")
    return CONTACT


async def choices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the selected function and asks for a photo.

    user is object class telegram._user.User

    incoming data user like: {
        'is_bot': bool
        'username': str
        'first_name': str
        'id': int(9 range)
        'language_code': str (like 'ru')
        }

    context.user_data["choice"] = text <- (saving choice user)
    """
    user = update.message.from_user
    text = update.message.text
    if text == "Получить информацию":
        await update.message.reply_text(
            "Пришлите qr-code устройства 🖥 ⌨️ 🖨, сотрудника 👨 👩 или помещения 🏢",
            reply_markup=ReplyKeyboardRemove(),
        )
        return DETAIL
    context.user_data["choice"] = text
    context.user_data["photos_device"] = []
    logger.info(f"Choices of {user.first_name}: {update.message.text}")
    await update.message.reply_text(
        "Пришлите qr-code офиса 🏢",
        reply_markup=ReplyKeyboardRemove(),
    )
    return OFFICE


async def next_employee_or_room(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["poll"] = ""
    if text == "Следующий сотрудник":
        context.user_data["photos_device"] = []
        await update.message.reply_text(
            "Пришлите qr-code сотрудника 👨 👩",
            reply_markup=ReplyKeyboardRemove(),
        )
        return PEOPLE
    elif text == "Следующее помещение":
        context.user_data["photos_device"] = []
        context.user_data["photo_office"] = ""
        await update.message.reply_text(
            "Пришлите qr-code офиса 🏢",
            reply_markup=ReplyKeyboardRemove(),
        )
        return OFFICE
    elif text == "Меню":
        context.user_data["photos_device"] = []
        context.user_data["photo_office"] = ""
        await update.message.reply_text(
            "Выберите нужную функцию",
            reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD, one_time_keyboard=True),
        )
        return CHOICES


async def photo_office(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    ask for qr-code office.
    """

    user = update.message.from_user
    file_name = f"./static_telegram/{user.id}-{NOW}-office.jpg"
    get_foto = await update.message.photo[-1].get_file()
    await get_foto.download_to_drive(file_name)
    logger.info(f"Photo of {user.first_name}: {file_name}")
    try:
        check_box = decode_image(file_name)
        if check_box[0] == "office":
            context.user_data["photo_office"] = check_box[1]  # add office to user data for further work
            await update.message.reply_text("Отлично, теперь пришлите мне qr-code сотрудника 👨 👩.")
            return PEOPLE
        else:
            await update.message.reply_text(
                f"Это qr-code {EMPLOYEE_OFFICE_DEVICE[check_box[0]]} 🔁\n"
                f"Пришлите пожалуйста qr-code офиса\nДля отмены нажмите -> /cancel"
            )

    except Exception as e:
        os.remove(file_name)
        await update.message.reply_text("Ваш qr-cod не распознан, попробуйте ещё раз 🔁")
        logger.info(f"Error of {user.first_name}: {e}")


async def photo_people(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ask for qr-code people."""

    user = update.message.from_user
    get_foto = await update.message.photo[-1].get_file()
    file_name = f"./static_telegram/{user.id}-{NOW}-people.jpg"
    await get_foto.download_to_drive(file_name)
    logger.info(f"Photo of {user.first_name}: {file_name}")
    try:
        check_box = decode_image(file_name)
        if check_box[0] == "employee":
            context.user_data["photo_people"] = check_box[1]
            await update.message.reply_text("Отлично, теперь пришлите мне qr-code устройств 🖥 ⌨️ 🖨")
            return COMPUTER
        else:
            await update.message.reply_text(
                f"Это qr-code {EMPLOYEE_OFFICE_DEVICE[check_box[0]]} 🔁\n"
                f"Пришлите пожалуйста qr-code сотрудника\nДля отмены нажмите -> /cancel"
            )

    except Exception as e:
        os.remove(file_name)
        logger.info(f"Error of {user.first_name}: {e}")
        await update.message.reply_text("Ваш qr-cod не распознан, попробуйте ещё раз 🔁")


async def photo_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ask for qr-code computer."""

    choice = context.user_data["choice"]
    choice_dict = {
        "Сверка": "Для завершения сверки устройств с сотрудником ",
        "Перемещение": "Для завершения перемещения устройств к сотруднику ",
        "Учёт": "Для завершения учёта устройств сотрудника",
    }
    user = update.message.from_user
    get_foto = await update.message.photo[-1].get_file()
    file_name = f"./static_telegram/{user.id}-{NOW}-computer.jpg"
    await get_foto.download_to_drive(file_name)
    logger.info(f"Photo of {user.first_name}: {file_name}")
    try:
        check_box = decode_image(file_name)
        if check_box[0] == "device":
            if check_box[1] in context.user_data["photos_device"]:
                await update.message.reply_text(
                    f"Данный qr-cod Вы уже сканировали, попробуйте другой. 🔁\n"
                    f"Для отмены нажмите /cancel\n{choice_dict[choice]} нажмите /next"
                )
                return COMPUTER
            else:
                context.user_data["photos_device"].append(check_box[1])
                await update.message.reply_text(
                    f"Qr-cod принят ✅\n\nОтсканируйте следующее устройство.\n"
                    f"{choice_dict[choice]} нажмите /next\nДля выхода из сверки нажмите /cancel."
                )
                return COMPUTER
        else:
            await update.message.reply_text(
                f"Это qr-code {EMPLOYEE_OFFICE_DEVICE[check_box[0]]}\n\n"
                f"Пришлите пожалуйста qr-code устройств\nДля отмены нажмите /cancel\n"
                f"{choice_dict[choice]} нажмите /next"
            )

    except Exception as e:
        logger.info(f"Error of {user.first_name}: {e}")
        os.remove(file_name)
        await update.message.reply_text("Ваш qr-cod не распознан, попробуйте ещё раз 🔁")


async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    delete_all_image(user_id)
    user_data = context.user_data["choice"]

    all_devices = context.user_data["photos_device"]
    user = context.user_data["photo_people"]
    office = context.user_data["photo_office"]
# --------------------------------УЧЕТ------------------------------------------
    if user_data == "Учёт":
        data = await insert_inventory_card(all_devices, user, office)
        bio_employee = await select_bio_employee(user)
        # 1) if there are no unaccounted for, then just send a message
        if data["не учтён"] == []:
            for i in data["учтён"]:
                await update.message.reply_text(i, parse_mode="HTML")
            await update.message.reply_text(
                "Выберите нужную фунцию",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_NEXT, one_time_keyboard=True),
            )
            return NEXT_EMPLOYEE_OR_ROOM

        # 2) if there are accounted for and not accounted for
        elif data["учтён"] != [] and data["не учтён"] != []:
            context.user_data["poll"] = data["uid"]
            context.user_data["poll"]["choice"] = "Учёт"
            for i in data["учтён"]:
                await update.message.reply_text(i, parse_mode="HTML")
            for i in data["не учтён"]:
                await update.message.reply_text(i, parse_mode="HTML")
            devices_n = 'устройства' if len(data["не учтён"]) > 1 else 'устройство'
            await update.message.reply_text(
                f"Желаете перезакрепить {devices_n} за сотрудником {bio_employee}? 🤔",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_YES_NOT, one_time_keyboard=True),
            )
            return POOL

        # 3) there are only unaccounted for
        elif data["учтён"] == [] and data["не учтён"] != []:
            context.user_data["poll"] = data["uid"]
            context.user_data["poll"]["choice"] = "Учёт"
            # 3.1) check if more than 1 device
            if len(data["не учтён"]) > 1:
                await update.message.reply_text("Устройства уже были учтены, желаете их перезакрепить? 😐")
                for i in data["не учтён"]:
                    await update.message.reply_text(i, parse_mode="HTML")
                    delete_all_image(user_id)
                await update.message.reply_text(
                    f"Желаете перезакрепить устройства за сотрудником {bio_employee}? 🤔",
                    reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_YES_NOT, one_time_keyboard=True),
                )
                return POOL
            # 3.2) if 1
            else:
                await update.message.reply_text("Устройство уже было учтено 😐")
                await update.message.reply_text(data["не учтён"][0], parse_mode="HTML")
                await update.message.reply_text(
                    f"Желаете перезакрепить устройство за сотрудником {bio_employee}? 🤔?",
                    reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_YES_NOT, one_time_keyboard=True),
                )
                return POOL
# ------------------------------------------------------------------------------

# ----------------------------------СВЕРКА--------------------------------------
    elif user_data == "Сверка":
        bio_employee = await select_bio_employee(user)
        data = await select(all_devices, user, office)

        # 1) if there are no unaccounted for, then just send a message
        if data["не учтён"] == []:
            for i in data["учтён"]:
                await update.message.reply_text(i, parse_mode="HTML")
            delete_all_image(user_id)
            await update.message.reply_text(
                "Выберите нужную фунцию",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_NEXT, one_time_keyboard=True),
            )
            return NEXT_EMPLOYEE_OR_ROOM

        # 2) if there are accounted for and not accounted for
        elif data["учтён"] != [] and data["не учтён"] != []:
            context.user_data["poll"] = data["uid"]
            context.user_data["poll"]["choice"] = "Сверка"
            for i in data["учтён"]:
                await update.message.reply_text(i, parse_mode="HTML")
            for i in data["не учтён"]:
                await update.message.reply_text(i, parse_mode="HTML")
            devices_y = "устройства" if len(data["не учтён"]) > 1 else "устройство"
            await update.message.reply_text(
                f"Желаете учесть {devices_y} за сотрудником {bio_employee}? 🤔",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_YES_NOT, one_time_keyboard=True),
            )
            return POOL

        # 3) there are only unaccounted for
        elif data["учтён"] == [] and data["не учтён"] != []:
            context.user_data["poll"] = data["uid"]
            context.user_data["poll"]["choice"] = "Сверка"
            devices_v = "устройства" if len(data["не учтён"]) > 1 else "устройство"
            choise_v = "учтённые" if len(data["не учтён"]) > 1 else "учтённое"
            await update.message.reply_text(f"Есть не {choise_v} {devices_v} 😐")
            for i in data["не учтён"]:
                await update.message.reply_text(i, parse_mode="HTML")
                delete_all_image(user_id)
            await update.message.reply_text(
                f"Желаете учесть {devices_v} за сотрудником {bio_employee}? 🤔",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_YES_NOT, one_time_keyboard=True),
            )
            return POOL
# ------------------------------------------------------------------------------

# ---------------------------ПЕРЕМЕЩЕНИЕ----------------------------------------
    elif user_data == "Перемещение":
        response = await movents(all_devices, user, office)
        if response["учтён"] != []:
            for device in response["учтён"]:
                await update.message.reply_text(device, parse_mode="HTML")
        elif response["не учтён"] != []:
            for device in response["не учтён"]:
                await update.message.reply_text(device, parse_mode="HTML")
        await update.message.reply_text(
            "Выберите нужную фунцию",
            reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_NEXT, one_time_keyboard=True),
        )
        return NEXT_EMPLOYEE_OR_ROOM
# ------------------------------------------------------------------------------


async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None or int:
    """Sends a predefined poll"""

    text = update.message.text
    devices = context.user_data["poll"]["devices"]
    employee = context.user_data["poll"]["employee"]
    office = context.user_data["poll"]["office"]
    choice = context.user_data["poll"]["choice"]
    choice_dict = {"Сверка": "Учёт не проведён", "Учёт": "Перемещение не проведено"}
    if text == "Да":
        if len(devices) > 1:
            questions = context.user_data["poll"]["name_model"]
            message = await context.bot.send_poll(
                update.effective_chat.id,
                "Какие устройства выбрать для учёта за сотрудником 🤔?"
                if choice == "Сверка"
                else "Какие устройства переместить  🤔?",
                questions,
                is_anonymous=False,
                allows_multiple_answers=True,
            )
            # Save some info about the poll the bot_data for later use in receive_poll_answer
            payload = {
                message.poll.id: {
                    "questions": questions,
                    "message_id": message.message_id,
                    "chat_id": update.effective_chat.id,
                    "answers": 0,
                }
            }
            context.bot_data.update(payload)
        else:
            if choice == "Сверка":
                response = await insert_inventory_card(devices, employee, office)
            else:
                response = await movents(devices, employee, office)
            await update.message.reply_text(response["учтён"][0], parse_mode="HTML")

            await update.message.reply_text(
                "Выберите нужную фунцию",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_NEXT, one_time_keyboard=True),
            )
            return NEXT_EMPLOYEE_OR_ROOM

    elif text == "Нет":
        await update.message.reply_text(choice_dict[choice])
        await update.message.reply_text(
            "Выберите нужную фунцию",
            reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_NEXT, one_time_keyboard=True),
        )
        return NEXT_EMPLOYEE_OR_ROOM


async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None or int:
    """Summarize a users poll vote"""

    answer = update.poll_answer
    choice = context.user_data["poll"]["choice"]
    answered_poll = context.bot_data[answer.poll_id]  # answer.poll_id = '5321011176010678462'
    try:
        answered_poll["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids  # list int like this -> [0, 1, ...]
    all_devices = context.user_data["poll"]["devices"]  # uids device
    employee = context.user_data["poll"]["employee"]  # uid employee
    office = context.user_data["poll"]["office"]  # uid office
    selected_devices = []  # only those devices selected by the user
    for num in selected_options:
        selected_devices.append(all_devices[num])
    if choice == "Сверка":
        response = await insert_inventory_card(selected_devices, employee, office)
    elif choice == "Учёт":
        response = await movents(selected_devices, employee, office)
    for device in response["учтён"]:
        await context.bot.send_message(
            answered_poll["chat_id"],
            device,
            parse_mode="HTML",
        )
    await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])
    await context.bot.send_message(
        chat_id=answered_poll["chat_id"],
        text="Выберите нужную фунцию",
        reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_NEXT, one_time_keyboard=True),
    )
    return NEXT_EMPLOYEE_OR_ROOM


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation.")
    await update.message.reply_text("Хорошего дня!", reply_markup=ReplyKeyboardRemove())

    # if user types /cancel in chat without reaching the end
    delete_all_image(user.id)
    return ConversationHandler.END


async def detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    get_foto = await update.message.photo[-1].get_file()
    file_name = f"./static_telegram/{user.id}-{NOW}-detail.jpg"
    await get_foto.download(file_name)
    logger.info(f"Photo of {user.first_name}: {file_name}")
    try:
        check_box = decode_image(file_name)
        os.remove(file_name)
        if check_box[0] == "device":
            result = await detail_device(check_box[1])
            await update.message.reply_text(f"{result}", parse_mode="HTML")
            await update.message.reply_text(
                "Выберите нужную фунцию",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD, one_time_keyboard=True),
            )
            return CHOICES
        elif check_box[0] == "office":
            context.user_data["office_detail"] = check_box[1]
            result = await detail_office(check_box[1])
            await update.message.reply_text(f"{result}", parse_mode="HTML")
            await update.message.reply_text(
                "Хотите подробный отчёт?",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD_YES_NOT, one_time_keyboard=True),
            )
            return DETAIL_CHOICE

        elif check_box[0] == "employee":
            context.user_data["employee_detail"] = check_box[1]
            result = await detail_employee(check_box[1])
            await update.message.reply_text(f"{result}", parse_mode="HTML")
            await update.message.reply_text(
                "Выберите нужную фунцию",
                reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD, one_time_keyboard=True),
            )
            return CHOICES

        else:
            await update.message.reply_text(
                "Ваш qr-cod не распознан, попробуйте прислать его ещё раз 🔁\n" "Либо нажмите /cancel для выхода"
            )
            return DETAIL

    except Exception as e:
        logger.info(f"Error of {user.first_name}: {e}")
        os.remove(file_name)
        await update.message.reply_text(
            "Ваш qr-cod не распознан, попробуйте ещё раз 🔁\n" "Либо нажмите /cancel для выхода"
        )
        return DETAIL


async def detail_choices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    office = context.user_data["office_detail"]
    if text == "Да":
        result = await detail_office_all(office)
        await update.message.reply_text(result, parse_mode="HTML")
    else:
        office = ""
        await update.message.reply_text(
            "Выберите нужную фунцию",
            reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD, one_time_keyboard=True),
        )
    return CHOICES


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    con = (
        update.message.contact
    )  # like contact {'user_id': 358519422, 'first_name': 'Оля', 'phone_number': '79119998877'}
    result = await update_chat_id([con["user_id"], con["phone_number"]])  # True or False
    if result:
        await update.message.reply_text("Ваш телефон принят.")
        await update.message.reply_text(
            "Выберите нужную фунцию", reply_markup=ReplyKeyboardMarkup(REPLY_KEYBOARD, one_time_keyboard=True)
        )
        return CHOICES
    else:
        await update.message.reply_text("У вас нет доступа.\nОбратитесь к администратору для добавления Вас в Базу.")
        await update.message.reply_text("Для старта бота нажмите /start, либо в левом нижнем углу выберите пункт меню")
        return ConversationHandler.END


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Для старта бота нажмите /start, либо в левом нижнем углу выберите пункт меню")


async def office_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Пришлите пожалуйста QR-cod офиса 🏢.\nДля выхода нажмите /cancel")


async def employee_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Пришлите пожалуйста QR-cod сотрудника 👨 👩.\nДля выхода нажмите /cancel")


async def device_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Пришлите пожалуйста QR-cod устройств 🖥 ⌨️ 🖨.\nДля выхода нажмите /cancel")


async def next_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Я вас не понимаю, выберите нужную функцию внизу экрана\nДля выхода нажмите /cancel"
    )


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOICES: [
                MessageHandler(filters.Regex("^(Сверка|Учёт|Перемещение|Получить информацию)$"), choices),
                MessageHandler(filters.Regex("^Выход$"), cancel),
                CommandHandler("start", next_help),
            ],
            OFFICE: [
                MessageHandler(filters.PHOTO, photo_office),
                CommandHandler("cancel", cancel),
                MessageHandler(filters.TEXT, office_help),
            ],
            PEOPLE: [
                MessageHandler(filters.PHOTO, photo_people),
                CommandHandler("cancel", cancel),
                MessageHandler(filters.TEXT, employee_help),
            ],
            COMPUTER: [
                MessageHandler(filters.PHOTO, photo_computer),
                CommandHandler("cancel", cancel),
                CommandHandler("next", next),
                MessageHandler(filters.TEXT, device_help),
            ],
            POOL: [MessageHandler(filters.Regex("^(Да|Нет)$"), poll), PollAnswerHandler(receive_poll_answer)],
            NEXT_EMPLOYEE_OR_ROOM: [
                MessageHandler(
                    filters.Regex("^(Следующий сотрудник|Следующее помещение|Меню)$"), next_employee_or_room
                ),
                MessageHandler(filters.Regex("^Выход$"), cancel),
                CommandHandler("cancel", cancel),
                MessageHandler(filters.TEXT, next_help),
            ],
            DETAIL: [MessageHandler(filters.PHOTO, detail), CommandHandler("cancel", cancel)],
            DETAIL_CHOICE: [
                MessageHandler(filters.Regex("^(Да|Нет)$"), detail_choices),
                CommandHandler("cancel", cancel),
            ],
            CONTACT: [MessageHandler(filters.CONTACT, contact), CommandHandler("cancel", cancel)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_chat=False,
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT, help))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
