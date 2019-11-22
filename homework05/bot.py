import calendar
import datetime
from collections import defaultdict
from typing import Dict, List

import requests
import telebot
from bs4 import BeautifulSoup
from telebot import apihelper

import config

bot = telebot.TeleBot(config.access_token)

apihelper.proxy = config.proxy

DEFAULT_GROUP = 'K3140'

WEEKDAYS = [name.lower() for name in calendar.day_name]

WEEKDAYS_RU = [
    'понедельник', 'вторник',
    'среду', 'четверг',
    'пятницу', 'субботу',
    'воскресенье', 'остальные дни'
]

WEEKDAYS_ITMO = {
    'Пн': 0, 'Вт': 1,
    'Ср': 2, 'Чт': 3,
    'Пт': 4, 'Сб': 5,
    '': 7,
}

EMOJI = {
    'teacher': u'\U0001F393',
    'location': u'\U0001F4CD',
    'sad': u'\U0001F612',
}

CACHE = defaultdict()


class Lesson:
    def __init__(self, time, for_week, location, lesson_name):
        self.time = time

        if for_week == 'нечетная неделя':
            self.week = 2

        elif for_week == 'четная неделя':
            self.week = 1

        else:
            self.week = 0

        self.location = location
        self.lesson_name = lesson_name


class Day:
    def __init__(self, weekday: int, lessons: List[Lesson]):
        self.weekday = weekday
        self.lessons = lessons

    def get_lessons_for_week(self, week: int):
        tuple_filter = (0, 1, 2) if week == 0 else (0, week)
        lessons = [lesson for lesson in self.lessons if lesson.week in tuple_filter]
        return Day(weekday=self.weekday, lessons=lessons)


class Schedule:
    def __init__(self, group: str):
        self.group = group

        self.days: List[Day] = []

    def load_data(self):
        page_content = get_schedule_page(self.group)

        soup = BeautifulSoup(page_content, "html.parser")

        days_content = soup.find_all('div', attrs={'class': 'rasp_tabl_day'})

        for day_content in days_content:
            day_data = self._parse_schedule_for_day(day_content)
            day = Day(weekday=day_data['weekday'], lessons=day_data['lessons'])
            self.days.append(day)

    @staticmethod
    def _parse_schedule_for_day(day_content) -> Dict:
        # Получаем таблицу с расписанием
        schedule_table = day_content.find("table")

        weekday = schedule_table.find("th", attrs={"class": "day"}).span.text
        weekday = WEEKDAYS_ITMO[weekday]

        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        for_week_list = [time.dt.text for time in times_list]
        times_list = [time.span.text for time in times_list]

        lessons_count = len(times_list)

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join(
            [
                ' '.join(
                    map(lambda name: name.strip(),
                        info.strip()
                        .replace('нечетная неделя', '')
                        .replace('четная неделя', '')
                        .split('\n'))
                ) for info in lesson_info if info
            ]
        ) for lesson_info in lessons_list]

        lessons = [
            Lesson(

                time=times_list[index],
                for_week=for_week_list[index],
                location=locations_list[index],
                lesson_name=lessons_list[index],
            ) for index in range(lessons_count)
        ]

        return {
            'weekday': weekday,
            'lessons': lessons,
        }

    @staticmethod
    def _get_week_number(datetime_object: datetime):
        return (datetime_object.isocalendar()[1] - 34) % 2 + 1

    def _get_week_days(self, week: int):
        return [day.get_lessons_for_week(week) for day in self.days]

    def _get_response_for_lesson(self, lesson: Lesson, week_label=True):
        *name, teacher = lesson.lesson_name.split('  ')

        if name:
            name = ' '.join(name)
            emoji_teacher = EMOJI['teacher']
            teacher = '%s %s\n' % (emoji_teacher, teacher if teacher else '')

        else:
            name = teacher
            teacher = ''

        location_emoji = EMOJI['location']

        if lesson.week == 1 and week_label:
            week = ' чет. |'
        elif lesson.week == 2 and week_label:
            week = ' нечет. |'
        else:
            week = ''

        return '_{time}_ |{week} *{lesson_name}*\n{location_emoji} {location}\n{teacher}'.format(
            time=lesson.time,
            week=week,
            lesson_name=name,
            location_emoji=location_emoji,
            location=lesson.location,
            teacher=teacher
        )

    def _get_response_for_day(self, day: Day, week_label=False):
        if day.lessons:
            response = 'Расписание на *%s*:\n\n' % WEEKDAYS_RU[day.weekday]

            lessons = [self._get_response_for_lesson(lesson, week_label) for lesson in day.lessons]

            response += '\n'.join(lessons)

        else:
            response = 'На *%s* нет пар *(Отдыхай)*\n' % WEEKDAYS_RU[day.weekday]

        return response

    @property
    def _group_label(self):
        return '`Группа` `%s`\n\n' % self.group

    def get_response_for_near(self, datetime_object: datetime):
        weekday = datetime_object.weekday()
        week = self._get_week_number(datetime_object)

        week_days = self._get_week_days(week)

        next_week = 1 if week == 2 else 2
        next_week_days = self._get_week_days(next_week)

        for day in next_week_days:
            day.weekday += 7

        week_days += next_week_days

        next_days = []
        for offset in range(6):
            for day in week_days:
                if next_days:
                    next_days.append(day)

                elif day.weekday == weekday + offset:
                    next_days.append(day)

            if next_days:
                break

        if next_days:
            for day in next_days:
                for lesson in day.lessons:
                    start, _ = [list(map(int, time.split(':'))) for time in lesson.time.split('-')]

                    date = datetime_object + datetime.timedelta(day.weekday - weekday)

                    lesson_start = datetime.datetime(
                        year=date.year, month=date.month, day=date.day,
                        hour=start[0], minute=start[1]
                    )

                    if datetime_object > lesson_start:
                        continue

                    if datetime_object.date() == lesson_start.date():
                        minutes = (lesson_start - datetime_object).seconds // 60
                        hours = minutes // 60
                        minutes -= hours * 60

                        hours = '%s ч. ' % hours if hours else ''
                        minutes = '%s мин.' % minutes

                        added = 'сегодня через %s%s' % (hours, minutes)

                    else:
                        days = (lesson_start - datetime_object).days
                        added = 'через %s дн.' % days

                    response = 'Ближайшая пара *%s*\n\n' % added
                    response += self._get_response_for_lesson(lesson)
                    return self._group_label + response

        sad_emoji = EMOJI['sad']
        return self._group_label + 'Ближайшой пары найти *не удалось* %s' % sad_emoji

    def get_response_for_day(self, datetime_object: datetime, week=None):
        if week is None:
            week = self._get_week_number(datetime_object)

        week_days = self._get_week_days(week)

        weekday = datetime_object.weekday()

        for day in week_days:
            if day.weekday == weekday:
                return self._group_label + self._get_response_for_day(day, week == 0)

        return self._group_label + 'На *%s* нет пар' % WEEKDAYS_RU[weekday]

    def get_response_for_all(self, datetime_object: datetime, week=None):
        if week is None:
            week = self._get_week_number(datetime_object)

        week_days = self._get_week_days(week)

        sep = '\n%s\n' % ('-' * 30)
        response = sep.join([self._get_response_for_day(day, week_label=week == 0) for day in week_days])
        return self._group_label + response


def get_page(group):
    url = '{domain}/{group}/raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        group=group
    )
    web_page = requests.get(url)
    return web_page.content


def parse_command(message: telebot.types.Message, page=None):
    print('New message from [%s]: %s' % (message.chat.id, message.text))

    parsed_args = message.text.split()

    try:
        if page == 'weekdays':
            length = len(parsed_args)

            if length == 3:
                day, week, group = parsed_args
                day = day.strip('/')
                week = int(week)

                return day, week, group

            elif length == 2:
                try:
                    day, week = parsed_args
                    day = day.strip('/')
                    week = int(week)

                    return day, week, None

                except ValueError:
                    day, group = parsed_args
                    day = day.strip('/')

                    return day, None, group

            elif length == 1:
                day = parsed_args[0]
                day = day.strip('/')

                return day, None, None

            else:
                raise ValueError

        elif page == 'all':
            parsed_args = parsed_args[1:]
            length = len(parsed_args)

            if length == 2:
                week, group = parsed_args
                week = int(week)

                return week, group

            elif length == 1:
                try:
                    week = parsed_args[0]
                    week = int(week)

                    return week, None

                except ValueError:
                    group = parsed_args[0]

                    return None, group

            else:
                return None, None

        else:
            parsed_args = parsed_args[1:]
            length = len(parsed_args)

            if length == 1:
                group = parsed_args[0]

                return group

            else:
                return None

    except ValueError:
        bot.send_message(message.chat.id, '*Неверный ввод!*', parse_mode='Markdown')
        return ()


def get_schedule_page(group):
    url = f'{config.domain}/{group}/raspisanie_zanyatiy_{group}.htm'
    return requests.get(url).content


def get_schedule_object(group: str or None) -> Schedule:
    if group is None:
        group = DEFAULT_GROUP

    if group not in CACHE:
        print('Load new schedule from server... [Group is %s]' % group)
        schedule = Schedule(group=group)
        schedule.load_data()

        CACHE[group] = schedule
        return schedule

    print('Return cached schedule... [Group is %s]' % group)
    schedule = CACHE[group]
    return schedule


@bot.message_handler(commands=WEEKDAYS)
def get_schedule(message: telebot.types.Message):
    """ Получить расписание на указанный день """
    try:
        day, week, group = parse_command(message, page='weekdays')

    except ValueError:
        return

    weekday = WEEKDAYS.index(day)
    day = datetime.datetime.now()

    while day.weekday() != weekday:
        day += datetime.timedelta(days=1)

    schedule = get_schedule_object(group=group)

    response = schedule.get_response_for_day(day, week)
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['near'])
def get_near_lesson(message: telebot.types.Message):
    """ Получить ближайшее занятие """
    try:
        group = parse_command(message)

    except ValueError:
        return

    day = datetime.datetime.now()

    schedule = get_schedule_object(group=group)

    response = schedule.get_response_for_near(day)
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message: telebot.types.Message):
    """ Получить расписание на следующий день """
    try:
        group = parse_command(message)

    except ValueError:
        return

    day = datetime.datetime.now() + datetime.timedelta(days=1)
    schedule = get_schedule_object(group=group)

    response = schedule.get_response_for_day(day)
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['all'])
def get_all_schedule(message: telebot.types.Message):
    """ Получить расписание на всю неделю для указанной группы """

    try:
        week, group = parse_command(message, page='all')

    except ValueError:
        return

    day = datetime.datetime.now()
    weekday = day.weekday()

    days_offset = 1 if weekday == 6 else -weekday
    day += datetime.timedelta(days=days_offset)

    schedule = get_schedule_object(group=group)
    response = schedule.get_response_for_all(day, week)

    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['weekday'])
def get_weekday(message: telebot.types.Message):
    response = "*Попробуйте ввести команды по типу:* \n\n%s" % (
        '\n'.join(map(lambda weekday: '/%s - _Получить расписание на %s_' % (
            weekday, WEEKDAYS_RU[WEEKDAYS.index(weekday)]
        ), WEEKDAYS))
    )
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def get_help(message: telebot.types.Message):
    response = "*Список доступных комманд:* \n\n" \
               "/weekday - _Получить расписание на указанный день_\n" \
               "/near - _Получить ближайшее занятие_\n" \
               "/tomorrow - _Получить расписание на следующий день_\n" \
               "/all - _Получить расписание на всю неделю для указанной группы_\n" \
               "/help - _Получить список доступных комманд_"
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
