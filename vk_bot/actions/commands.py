from pprint import pprint

from vkbottle.bot import Message
from tools import keyboards


async def start(ans: Message, chat_id: int, storage):
    """Команда бота Начать"""
    # Проверяем есть пользователь в базе данных
    if storage.get_vk_user(chat_id):
        storage.delete_vk_user_or_userdata(chat_id)  # Удаляем пользвателя из базы данных
    await ans.answer('Привет\n')
    await ans.answer('Для начала пройдите небольшую регистрацию😉\n')
    await ans.answer('Выберите институт.', keyboard=keyboards.make_keyboard_institutes(storage.get_institutes()))


async def registration(ans: Message, chat_id: int, storage):
    """Команда бота Регистрация"""
    # Проверяем есть пользователь в базе данных
    if storage.get_vk_user(chat_id):
        storage.delete_vk_user_or_userdata(chat_id)  # Удаляем пользвателя из базы данных
    await ans.answer('Повторная регистрация😉\n')

    keyboard = keyboards.make_keyboard_institutes(storage.get_institutes())
    pprint(keyboard)

    await ans.answer('Выберите институт.', keyboard=keyboard)


async def show_map(ans: Message, photo_vk_name: str):
    """Команда бота Карта"""
    await ans.answer('Карта университета', attachment=f'{photo_vk_name}',
                     keyboard=keyboards.make_keyboard_start_menu())


async def authors(ans: Message):
    """Команда бота Авторы"""
    await ans.answer('Авторы проекта:\n'
                     '-[id132677094|Алексей]\n'
                     '-[id128784852|Султан]\n'
                     '-[id169584462|Александр] \n'
                     '-[id135615548|Владислав]\n'
                     '-[id502898628|Кирилл]\n\n'
                     'По всем вопросом и предложениям пишите нам в личные сообщения. '
                     'Будем рады 😉\n', keyboard=keyboards.make_keyboard_start_menu()
                     )


async def tip(ans: Message):
    """Команда бота Подсказка"""
    await ans.answer('Здравствуйте! Раз Вы вызвали Подсказку еще раз, значит дело серьезное.😬\n\n'
                     'Напомню Вам основные советы по использованию бота:\n'
                     '⏭Используйте кнопки, так я буду Вас лучше понимать!\n\n'
                     '🌄Подгружайте расписание утром и оно будет в нашем чате до скончания времен!\n\n'
                     '📃Чтобы просмотреть список доступных команд и кнопок, напишите в чате [Помощь]\n\n'
                     '🆘Чтобы вызвать эту подсказку снова, напиши в чат [Подсказка] \n\n'
                     'Если Вы столкнулись с технической проблемой, то Вы можете:\n'
                     '- обратиться за помощью в официальную группу ВКонтакте [https://vk.com/smartschedule]\n'
                     '- написать одному из моих создателей (команда Авторы)🤭\n',
                     keyboard=keyboards.make_keyboard_start_menu()
                     )


async def tip(ans: Message):
    """Команда бота Подсказка"""
    await ans.answer('Здравствуйте! Раз Вы вызвали Подсказку еще раз, значит дело серьезное.😬\n\n'
                     'Напомню Вам основные советы по использованию бота:\n'
                     '⏭Используйте кнопки, так я буду Вас лучше понимать!\n\n'
                     '🌄Подгружайте расписание утром и оно будет в нашем чате до скончания времен!\n\n'
                     '📃Чтобы просмотреть список доступных команд и кнопок, напишите в чате [Помощь]\n\n'
                     '🆘Чтобы вызвать эту подсказку снова, напиши в чат [Подсказка] \n\n'
                     'Если Вы столкнулись с технической проблемой, то Вы можете:\n'
                     '- обратиться за помощью в официальную группу ВКонтакте [https://vk.com/smartschedule]\n'
                     '- написать одному из моих создателей (команда Авторы)🤭\n',
                     keyboard=keyboards.make_keyboard_start_menu()
                     )


async def help(ans: Message):
    """Команда бота Помощь"""
    await ans.answer('Список доступных Вам команд, для использования просто напишите их в чат😉:\n'
                     'Старт – запустить диалог с ботом сначала\n'
                     'Регистрация – пройти регистрацию заново\n'
                     'Карта – карта корпусов ИРНИТУ\n'
                     'О проекте – краткая информация о боте\n'
                     'Авторы – мои создатели\n'
                     'Подсказка – подсказка (как неожиданно🙃)\n'
                     'Помощь – список доступных команд\n',
                     keyboard=keyboards.make_keyboard_start_menu()
                     )
