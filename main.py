from bitrix24 import Bitrix24, BitrixError
import asyncio
from datetime import date, timedelta
import time
from isdayoff import DateType, ProdCalendar

Red = "\033[31m"
Yellow = "\033[33m"
Green = "\033[32m"
reset = '\033[0m'

bx24 = Bitrix24('https://b24-hzzdt4.bitrix24.kz/rest/1/84tcvbk479gmj6xu/')
day = date.today() + timedelta(days=3)


async def weekend_check():
    """
    Функция проверки выходных дней
    :return : String
    """
    if await ProdCalendar(locale='ru').date(day) == DateType.WORKING:
        return f'{Yellow}Рабочий день'
    else:
        try:
            # проверяем наличие задачи по тексту и дате, если задачинет создаем новую задачу
            title_list = []
            all_tasks = bx24.callMethod('tasks.task.list')
            for i in all_tasks['tasks']:
                title_list.append(i['title'])
            if f'Поздравить наших клиентов - {day}' not in title_list:
                bx24.callMethod('tasks.task.add',
                                fields={
                                    'TITLE': f'Поздравить наших клиентов - {day}',
                                    'RESPONSIBLE_ID': 1
                                })

                return f'{Red}Выходной день,{reset} задача добавлена!'
        except BitrixError as ex:
            return ex
        return f'{Red}Выходной день'


def write_log(date, isDay):
    """
    Запись логов в MyLog.txt
    :param date: String
    :param isDay: String
    :return: None
    """
    with open('MyLog.txt', 'a') as f:
        f.write(f'{date} это {isDay}\n')
        print(f'{Green}{date}{reset} это {isDay}! \n{reset}')
        f.close()


# Бесконечный цикл для череды функции проверки и паузы
my_var = day.strftime("%A %d. %B %Y")
while True:
    write_log(my_var, asyncio.run(weekend_check()))
    my_var = time.sleep(86400)
    my_var = day.strftime("%A %d. %B %Y")
