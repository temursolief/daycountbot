import datetime
import logging

import pytz
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    """Sends explanation on how to use the bot."""
    msg = 'Hi, {user.mention_markdown_v2()}! \nUse /today to know the cardinal number of the day and week of this year.\n\nTo schedule something, type /schedule first, and then enter the time and the date you wanna be notified in this format:\n12:00 01 10 2022\n\ntime\day\month\year\ \nFrom a new line, enter your message to your future\n For example: /schedule 12:00 10 12 2022\nToday I need to go to the birthday of ma friend'
    update.message.reply_text(msg)

TOKEN = "TELEGRAM_TOKEN"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

current_date = datetime.datetime.now()
day_of_year = current_date.timetuple().tm_yday
week_of_year = datetime.datetime.isocalendar(current_date)[1]
year = current_date.timetuple().tm_year


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        'This bot helps you to stay organized with your time and schedules\nIf you want to know how to use it, please, push the /start button'
    )
todayText=""


def today_command(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.message.chat_id

    global todayText
    todayText = 'Today is the day number {0} in the week number {1} in the year {2}'.format(day_of_year, week_of_year, year)

    update.message.reply_text(todayText)
    context.job_queue.run_daily(daily_reminder, time=datetime.time(hour=14, minute=13, second=0, microsecond=0, tzinfo=pytz.timezone("Asia/Tashkent"), fold=0), context=chat_id)


def daily_reminder(context: CallbackContext):
    job = context.job
    context.bot.send_message(job.context, text=todayText)


def schedule_command(update: Update, context: CallbackContext):

    user = update.message.from_user

    try:
        message = update.message.text.split(' ')
        time = message[1]
        hour = int(time[:2])
        minute = int(time[2:4])
        day = int(time[4:6])
        month = int(time[6:8])
        year = int(time[8:12])

        date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0, tzinfo=pytz.timezone("Asia/Tashkent"))

        global note
        note = " ".join(message[2::])

        update.message.reply_markdown_v2(f'Dear {user.mention_markdown_v2()} I will notify you on the given date')
        print(date)
        print(type(date))
        context.job_queue.run_once(notify, date, context=chat_id)


    except Exception as err:
        print(err)
        user.send_message("Please, follow the instructions to schedule")


def notify(context: CallbackContext):
    job = context.job
    context.bot.send_message(job.context, text=note)


def main():
    """Start the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler("today", today_command))
    dispatcher.add_handler(CommandHandler('schedule', schedule_command))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, start))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
