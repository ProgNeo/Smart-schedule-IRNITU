from tools.tg_tools import keyboards
from tools import statistics
from db import postgre_storage


def start(bot, message, storage, tz):
    """Команда бота Начать"""
    chat_id = message.chat.id

    # Проверяем есть пользователь в базе данных
    if storage.get_user(chat_id):
        # Удаляем пользвателя из базы данных
        storage.delete_user_or_userdata(chat_id)

    bot.send_message(chat_id=chat_id, text='Для начала пройдите небольшую регистрацию\n'
                                           'Кто вы?',
                     reply_markup=keyboards.make_inline_keyboard_choose_registration())

    statistics.add(action='start', storage=storage, tz=tz)


def registration(bot, message, storage, tz):
    """Команда бота Регистрация"""
    chat_id = message.chat.id
    storage.delete_user_or_userdata(chat_id=chat_id)
    bot.send_message(chat_id=chat_id, text='Пройдите повторную регистрацию\n'
                                           'Кто вы?',
                     reply_markup=keyboards.make_inline_keyboard_choose_registration())

    statistics.add(action='reg', storage=storage, tz=tz)


def show_map(bot, message, storage, tz):
    """Команда бота Карта"""
    chat_id = message.chat.id
    bot.send_photo(chat_id, (open('map.jpg', "rb")))
    statistics.add(action='map', storage=storage, tz=tz)


def authors(bot, message, storage, tz):
    """Команда бота Авторы"""
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, parse_mode='HTML',
                     text='<b>Авторы проекта:\n</b>'
                          '- Ярослав @ProgNeo'
                          '- Илья @ilmysko'
                          'По всем вопросом и предложениям пишите нам в личные сообщения.\n'
                     )
    statistics.add(action='authors', storage=storage, tz=tz)


def tip(bot, message, storage, tz):
    """Команда бота Подсказка"""
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, parse_mode='HTML',
                     text='Здравствуйте! Раз Вы вызвали Подсказку еще раз, значит дело серьезное.😬\n\n'
                     'Напомню Вам основные советы по использованию бота:\n'
                     '⏭ Используйте кнопки, так я буду Вас лучше понимать!\n\n'
                     '🌄 Подгружайте расписание утром и оно будет в нашем чате до скончания времен!\n\n'
                     '📃 Чтобы просмотреть список доступных команд и кнопок, напишите в чате [Помощь]\n\n'
                     '🆘 Чтобы вызвать эту подсказку снова, напиши в чат [Подсказка] \n\n'
                     'Если Вы столкнулись с технической проблемой, то Вы можете:\n'
                     '- обратиться за помощью в официальную группу ВКонтакте [https://vk.com/smartschedule]\n'
                     '- написать одному из моих создателей (команда Авторы)🤭\n'
                     )
    statistics.add(action='tip', storage=storage, tz=tz)


def help_info(bot, message, storage, tz):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Список доступных Вам команд, для использования просто напишите их в чат😉:\n'
                                           '/start – запустить диалог с ботом сначала\n'
                                           '/reg – пройти регистрацию заново\n'
                                           '/map – карта корпусов ИРНИТУ\n'
                                           '/about – краткая информация о боте\n'
                                           '/authors – мои создатели\n'
                                           '/tip – подсказка\n'
                                           '/help – список доступных команд\n'
                     )

    statistics.add(action='help', storage=storage, tz=tz)


def about(bot, message, storage, tz):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, parse_mode='HTML',
                     text='<b>О боте:\n</b>'
                          'Smart schedule IRNITU bot - это чат бот для просмотра расписания занятий в '
                          'Иркутском национальном исследовательском техническом университете\n\n'
                          '<b>Благодаря боту можно:\n</b>'
                          '- Узнать актуальное расписание\n'
                          '- Нажатием одной кнопки увидеть информацию о ближайшей паре\n'
                          '- Настроить гибкие уведомления с информацией из расписания, '
                          'которые будут приходить за определённое время до начала занятия')

    statistics.add(action='about', storage=storage, tz=tz)
