from bitrix24 import *
import asyncio
from pprint import pprint
from datetime import date, timedelta
from isdayoff import DateType, ProdCalendar

bx24 = Bitrix24('https://b24-hzzdt4.bitrix24.kz/rest/1/84tcvbk479gmj6xu/')
calendar = ProdCalendar(locale='ru')


async def main():
    if await calendar.date(date.today() + timedelta(days=3)) == DateType.WORKING:
        print("Рабочий день")
    else:
        try:
            bx24.callMethod('tasks.task.add',
                            fields={'TITLE': 'Поздравить ребят с наступающим праздником', 'RESPONSIBLE_ID': 1})
            pprint(bx24.callMethod('tasks.task.list'))
        except BitrixError as ex:
            print(ex)
        print("Скоро праздники")


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
