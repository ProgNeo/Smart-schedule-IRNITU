import datetime
import json
import os
import pathlib
from pathlib import Path

from db.api import data_conversion_api, postgre_storage_api
from tools.logger import logger


async def processing_api_schedule_two_weeks(bot, message):
    try:
        chat_id = message.chat.id
        text = message.text

        words = text.split('?')
        if len(words) > 1:
            data = datetime.datetime.strptime(words[1], '%Y-%m-%d')
        else:
            data = datetime.datetime.now()

        file_name = f'two_weeks-{data.strftime("%Y-%m-%d")}.json'
        response = data_conversion_api.convert_schedule_dict(postgre_storage_api.get_schedule(data))

        current_dir = pathlib.Path().resolve()

        Path(f'{current_dir}/api_responses/{chat_id}').mkdir(parents=True, exist_ok=True)
        file = open(f'{current_dir}/api_responses/{chat_id}/{file_name}', 'w')
        file.write(json.dumps(response, ensure_ascii=False))
        file.close()

        bot.send_document(
            chat_id=chat_id,
            document=open(f'{current_dir}/api_responses/{chat_id}/{file_name}'),
            timeout=90
        )
        os.remove(f'{current_dir}/api_responses/{chat_id}/{file_name}')
    except Exception as ex:
        logger.error(ex)


async def processing_api_schedule_month(bot, message):
    try:
        chat_id = message.chat.id
        text = message.text

        words = text.split('?')
        if len(words) > 2:
            year = int(words[1])
            month = int(words[2])
        else:
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year

        file_name = f'month-{year}-{month}.json'
        response = data_conversion_api.convert_schedule_dict(postgre_storage_api.get_schedule_month(year, month))

        current_dir = pathlib.Path().resolve()

        Path(f'{current_dir}/api_responses/{chat_id}').mkdir(parents=True, exist_ok=True)
        file = open(f'{current_dir}/api_responses/{chat_id}/{file_name}', 'w')
        file.write(json.dumps(response, ensure_ascii=False))
        file.close()

        bot.send_document(
            chat_id=chat_id,
            document=open(f'{current_dir}/api_responses/{chat_id}/{file_name}'),
            timeout=90
        )
        os.remove(f'{current_dir}/api_responses/{chat_id}/{file_name}')
    except Exception as ex:
        logger.error(ex)


async def processing_api(bot, message):
    chat_id = message.chat.id
    text = message.text

    response = '{"null": "0"}'
    file_name = f'response.json'

    try:
        match text:
            case '/api/institutes':
                file_name = 'institutes.json'
                response = data_conversion_api.convert_institutes_dict(postgre_storage_api.get_institutes())
            case '/api/groups':
                file_name = 'groups.json'
                response = data_conversion_api.convert_groups_dict(postgre_storage_api.get_groups())
            case '/api/lessons_time':
                file_name = 'lessons_time.json'
                response = data_conversion_api.convert_lessons_dict(postgre_storage_api.get_lessons())
            case '/api/teachers':
                file_name = 'teachers.json'
                response = data_conversion_api.convert_teachers_dict(postgre_storage_api.get_teachers())
            case '/api/lessons_names':
                file_name = 'lessons_names.json'
                response = data_conversion_api.convert_disciplines_dict(postgre_storage_api.get_disciplines())
            case '/api/classrooms':
                file_name = 'classrooms.json'
                response = data_conversion_api.convert_classrooms_dict(postgre_storage_api.get_classrooms())

        current_dir = pathlib.Path().resolve()

        Path(f'{current_dir}/api_responses/{chat_id}').mkdir(parents=True, exist_ok=True)
        file = open(f'{current_dir}/api_responses/{chat_id}/{file_name}', 'w')
        file.write(json.dumps(response, ensure_ascii=False))
        file.close()

        bot.send_document(
            chat_id=chat_id,
            document=open(f'{current_dir}/api_responses/{chat_id}/{file_name}'),
            timeout=90
        )
        os.remove(f'{current_dir}/api_responses/{chat_id}/{file_name}')
    except ValueError as error:
        logger.error(error)
