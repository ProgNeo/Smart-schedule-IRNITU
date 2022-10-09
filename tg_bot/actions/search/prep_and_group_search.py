from tools.tg_tools import keyboards, schedule_processing
from tools.schedule_tools import find_week, near_lesson, creating_schedule
from db.mongo_storage import MongodbService
import json

# Глобальная переменная(словарь), которая хранит в себе 3 состояния
# (номер страницы; слово, которые находим; список соответствия для выхода по условию в стейте)
Condition_request = {}
storage = MongodbService().get_instance()

def groups_exam(group):
    schedule = storage.get_schedule_exam(group=group)
    if not schedule:
        return 0
    del schedule['_id']
    clear_list = []
    for i in range(len(schedule['exams']['exams'])):
        if schedule['exams']['exams'][i] not in clear_list:
            clear_list.append(schedule['exams']['exams'][i])
    schedule['exams']['exams'] = clear_list
    return schedule

def start_search(bot, message, storage, tz):
    data = message.chat.id
    message_id = message.message_id
    # ID пользователя
    chat_id = message.chat.id
    # Создаём ключ по значению ID пользователя
    Condition_request[chat_id] = []
    # Зарашиваем данные о пользователе из базы
    user = storage.get_user(chat_id=chat_id)
    # Условие для проверки наличия пользователя в базе

    if user:

        # Запуск стейта со значением SEARCH
        msg = bot.send_message(chat_id=chat_id, text='Введите название группы или фамилию преподавателя\n'
                                                     'Например: ИБб-18-1 или Маринов',
                               reply_markup=keyboards.make_keyboard_main_menu())

        bot.register_next_step_handler(msg, search, bot=bot, tz=tz, storage=storage)

    else:

        bot.send_message(chat_id=chat_id, text='Привет\n')
        bot.send_message(chat_id=chat_id, text='Для начала пройдите небольшую регистрацию😉\n')
        bot.send_message(chat_id=chat_id, text='Выберите институт',
                         reply_markup=keyboards.make_inline_keyboard_choose_institute(storage.get_institutes()))


def search(message, bot, storage, tz, last_msg=None):
    """Регистрация преподавателя"""
    global Condition_request
    data = message
    chat_id = message.chat.id
    message = message.text
    all_found_groups = []
    all_found_prep = []
    page = 0

    if data.content_type == 'sticker':
        message = ''

    if last_msg:
        try:
            bot.delete_message(last_msg.chat.id, last_msg.message_id)
        except Exception as e:
            pass

    if storage.get_search_list(message) or storage.get_search_list_prep(message):
        # Результат запроса по группам
        request_group = storage.get_search_list(message)
        # Результат запроса по преподам
        request_prep = storage.get_search_list_prep(message)
        # Циклы нужны для общего поиска. Здесь мы удаляем старые ключи в обоих реквестах и создаём один общий ключ,
        # как для групп, так и для преподов
        for i in request_group:
            i['found_prep'] = i.pop('name')
        for i in request_prep:
            i['found_prep'] = i.pop('prep_short_name')
        # Записываем слово, которое ищем
        request_word = message
        # Склеиваем результаты двух запросов для общего поиска
        request = request_group + request_prep
        last_request = request[-1]
        # Отправляем в функцию данные для создания клавиатуры
        # Эти циклы записывают группы и преподов в нижнем регистре для удобной работы с ними
        for i in request_group:
            all_found_groups.append(i['found_prep'].lower())
        for i in request_prep:
            all_found_prep.append(i['found_prep'].lower())
        # Создаём общий список
        all_found_results = all_found_groups + all_found_prep
        # Формируем полный багаж для пользователя
        list_search = [page, request_word, all_found_results]
        # Записываем все данные под ключом пользователя
        Condition_request[chat_id] = list_search
        # Выводим результат поиска с клавиатурой (кливиатур формируется по поисковому запросу)
        if len(request) > 10:
            requests = request[:10 * (page + 1)]
            more_than_10 = True
            msg = bot.send_message(chat_id=chat_id, text='Результат поиска',
                                   reply_markup=keyboards.make_keyboard_search_group(last_request=last_request,
                                                                                     page=page,
                                                                                     more_than_10=more_than_10,
                                                                                     requests=requests))
            bot.register_next_step_handler(msg, search, bot=bot, storage=storage, tz=tz, last_msg=msg)

        else:
            msg = bot.send_message(chat_id=chat_id, text='Результат поиска',
                                   reply_markup=keyboards.make_keyboard_search_group(last_request=last_request,
                                                                                     page=page,
                                                                                     more_than_10=False,
                                                                                     requests=request))
            bot.register_next_step_handler(msg, search, bot=bot, storage=storage, tz=tz, last_msg=msg)

    elif ('На текущую неделю' == message or 'На следующую неделю' == message):
        group = Condition_request[chat_id][1]
        request_word = Condition_request[chat_id][1]
        request_group = storage.get_search_list(request_word)
        request_prep = storage.get_search_list_prep(request_word)
        # Если есть запрос для группы, то формируем расписание для группы, а если нет, то для препода
        if request_group:
            schedule = storage.get_schedule(group=group)
        elif request_prep:
            schedule = request_prep[0]
        if not schedule:
            bot.send_message(chat_id=chat_id, text='Расписание временно недоступно\nПопробуйте позже⏱')
            return

        schedule = schedule['schedule']
        week = find_week.find_week()

        # меняем неделю
        if message == 'На следующую неделю':
            week = 'odd' if week == 'even' else 'even'

        week_name = 'четная' if week == 'odd' else 'нечетная'
        if request_group:
            schedule_str = creating_schedule.full_schedule_in_str(schedule, week=week)
        elif request_prep:
            schedule_str = creating_schedule.full_schedule_in_str_prep(schedule, week=week)

        # Проверяем, что расписание сформировалось
        if isinstance(schedule_str, None):
            schedule_processing.sending_schedule_is_not_available(bot=bot, chat_id=chat_id)
            return


        bot.send_message(chat_id=chat_id, text=f'Расписание {group}\n'
                                               f'Неделя: {week_name}',
                         reply_markup=keyboards.make_keyboard_start_menu())
        # Отправка расписания
        schedule_processing.sending_schedule(bot=bot, chat_id=chat_id, schedule_str=schedule_str)

        bot.clear_step_handler_by_chat_id(chat_id=chat_id)

    elif 'Экзамены' == message:
        group = Condition_request[chat_id][1]
        request_word = Condition_request[chat_id][1]
        request_group = storage.get_search_list(request_word)
        request_prep = storage.get_search_list_prep(request_word)

        # Объявляем переменную с расписанием экзаменов группы или препода
        if request_group:
            schedule_str = groups_exam(group)
        elif request_prep:
            schedule_str = groups_exam(group)

        # При отсутствии расписания выводится соответствующее предупреждение
        if not schedule_str:
            bot.send_message(chat_id=chat_id, text='Расписание экзаменов отсутствует😇\nПопробуйте позже⏱')
            return

        # Задаем расписанию экзаменов вид для подачи пользователю
        schedule_exams = creating_schedule.schedule_view_exams(schedule=schedule_str)

        # Проверяем, что расписание сформировалось
        if isinstance(schedule_exams, None):
            schedule_processing.sending_schedule_is_not_available(bot=bot, chat_id=chat_id)
            return

        # Отправка расписания
        schedule_processing.sending_schedule(bot=bot, chat_id=chat_id, schedule_str=schedule_exams)

        bot.clear_step_handler_by_chat_id(chat_id=chat_id)

    elif 'Основное меню' == message:
        bot.send_message(chat_id=chat_id, text='Основное меню',
                         reply_markup=keyboards.make_keyboard_start_menu())

        bot.clear_step_handler_by_chat_id(chat_id=chat_id)

        return

    else:
        msg = bot.send_message(chat_id=chat_id, text='Проверьте правильность ввода 😞',
                               reply_markup=keyboards.make_keyboard_main_menu())
        bot.register_next_step_handler(msg, search, bot=bot, storage=storage, tz=tz, last_msg=msg)

    return




def handler_buttons(bot, message, storage, tz):
    """Обрабатываем колбэк преподавателя"""
    global Condition_request
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = json.loads(message.data)

    if data['prep_list'] == 'main':
        bot.send_message(chat_id=chat_id, text='Основное меню',
                         reply_markup=keyboards.make_keyboard_start_menu())
        try:
            bot.delete_message(message_id=message_id, chat_id=chat_id)
        except Exception as e:
            pass


        bot.clear_step_handler_by_chat_id(chat_id=chat_id)

        return

    # TODO: Если разберетесь для чего эта строка - удалите её
    try:
        if not Condition_request.get(chat_id) and len(Condition_request.get(chat_id)) != 0:
            Condition_request[chat_id][1] = ''
    except Exception as e:
        pass

    page = Condition_request[chat_id][0]
    request_word = Condition_request[chat_id][1]

    # Выходим из цикла поиска преподавателя по ФИО
    bot.clear_step_handler_by_chat_id(chat_id=chat_id)
    # Результат запроса по группам
    request_group = storage.get_search_list(request_word)
    # Результат запроса по преподам
    request_prep = storage.get_search_list_prep(request_word)
    # Циклы нужны для общего поиска. Здесь мы удаляем старые ключи в обоих реквестах и создаём один общий ключ,
    # как для групп, так и для преподов
    for i in request_group:
        i['found_prep'] = i.pop('name')
    for i in request_prep:
        i['found_prep'] = i.pop('prep_short_name')
    # Склеиваем результаты двух запросов для общего поиска
    request = request_group + request_prep

    last_request = request[-1]

    if data['prep_list'].lower() in Condition_request[chat_id][2]:
        try:
            bot.delete_message(message_id=message_id, chat_id=chat_id)
        except Exception as e:
            pass
        Condition_request[chat_id][1] = data['prep_list']
        des = message.data.split(":")[1].replace("}", "").replace('"', '')
        if "-" in data['prep_list'].lower():
            msg = bot.send_message(chat_id=chat_id, text=f'Выберите неделю для {des}',
                                   reply_markup=keyboards.make_keyboard_choose_schedule())
        else:
            msg = bot.send_message(chat_id=chat_id, text=f'Выберите неделю для {des}',
                                   reply_markup=keyboards.make_keyboard_choose_schedule_for_aud_search())
        bot.register_next_step_handler(msg, search, bot=bot, storage=storage, tz=tz, last_msg=msg)


    elif data['prep_list'] == 'back':
        more_than_10 = False
        if len(request) > 10:
            requests = request[10 * (page - 1):10 * page]
            more_than_10 = True

        if Condition_request[chat_id][0] - 1 == 0:
            try:
                bot.delete_message(message_id=message_id, chat_id=chat_id)
            except Exception as e:
                pass
            bot.send_message(chat_id=chat_id, text=f'Первая страница поиска:',
                             reply_markup=keyboards.make_keyboard_search_group(last_request=last_request,
                                                                               page=page - 1,
                                                                               requests=requests,
                                                                               more_than_10=more_than_10))

        else:
            bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                          reply_markup=keyboards.make_keyboard_search_group(last_request=last_request,
                                                                                            page=page - 1,
                                                                                            requests=requests,
                                                                                            more_than_10=more_than_10))
        Condition_request[chat_id][0] -= 1

    elif data['prep_list'] == 'next':
        try:
            bot.delete_message(message_id=message_id, chat_id=chat_id)
        except Exception as e:
            pass
        more_than_10 = False
        if len(request) > 10:
            requests = request[10 * (page + 1):10 * (page + 2)]
            more_than_10 = True
        bot.send_message(chat_id=chat_id, text=f'Следующая страница',
                         reply_markup=keyboards.make_keyboard_search_group(last_request=last_request,
                                                                           page=page + 1,
                                                                           requests=requests,
                                                                           more_than_10=more_than_10))
        Condition_request[chat_id][0] += 1

    # Регистрируем преподавателя по выбранной кнопке

    else:
        msg = bot.send_message(chat_id=chat_id, text='Проверьте правильность ввода 😞',
                               reply_markup=keyboards.make_keyboard_main_menu())
        bot.register_next_step_handler(msg, search, bot=bot, storage=storage, tz=tz, last_msg=msg)
