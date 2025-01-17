from pytz import timezone
from telebot import TeleBot

from db.mongo_storage import MongodbServiceTG
from tools.messages import registration_messages, other_messages
from tools.tg_tools import inline_keyboards


def start(bot: TeleBot, message, storage: MongodbServiceTG):
    chat_id = message.chat.id

    storage.delete_user_or_userdata(chat_id)
    bot.send_message(
        chat_id=chat_id,
        text=registration_messages['new_registration'],
        reply_markup=inline_keyboards.keyboard_user_role()
    )


def registration(bot: TeleBot, message, storage: MongodbServiceTG, edit: bool = False):
    chat_id = message.chat.id
    message_id = message.message_id

    storage.delete_user_or_userdata(chat_id)
    if not edit:
        bot.send_message(
            chat_id=chat_id,
            text=registration_messages['repeat_registration'],
            reply_markup=inline_keyboards.keyboard_user_role()
        )
    else:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=registration_messages['repeat_registration'],
            reply_markup=inline_keyboards.keyboard_user_role()
        )


def help(bot: TeleBot, message, storage: MongodbServiceTG):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text=other_messages['help_message']
    )


def about(bot: TeleBot, message, storage: MongodbServiceTG):
    chat_id = message.chat.id

    bot.send_message(
        chat_id=chat_id,
        parse_mode='HTML',
        text=other_messages['about_message']
    )


def show_map(bot: TeleBot, message, storage: MongodbServiceTG):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        text=other_messages['map_message']
    )


def authors(bot: TeleBot, message, storage: MongodbServiceTG):
    chat_id = message.chat.id

    bot.send_message(
        chat_id=chat_id,
        parse_mode='HTML',
        text=other_messages['author_message']
    )
