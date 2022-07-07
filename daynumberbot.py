import logging
import re
import time
import requests
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, JobQueue, Job

from datetime import date, time, datetime

TIME = '^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$'

TOKEN = "5470929952:AAEwtUHStfTEhwFt1oisEzBTnmfoxZCr4Es"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

current_date = datetime.now()
day_of_year = current_date.timetuple().tm_yday
week_of_year = datetime.isocalendar(current_date)[1]
year = current_date.timetuple().tm_year


def start(update:Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_markdown_v2(
        f"Hello, {user.mention_markdown_v2()} \nThis bot helps you to send the cardinal number of the date \n\n Use /today to know the day number of today"
        )


def help_command(update: Update, context: CallbackContext):
    update.message.reply_markdown_v2(
        'This bot helps you to stay organized with your time and schedules\nIf you want to know the day number of today then press /today\nIf you want to schedule something and wanna be notified on your appointments then follow these commands:\n\n"To schedule something, type /schedule first, and then enter the time and the date you wanna be notified in this format: \n12:00 01 10 2022\n\ntime\day\month\year\ \nFrom a new line, enter your message to your future\nFor example: /schedule 12:00 10 12 2022\nToday I need to go to the birthday of ma friend"'
    )


def today_command(update: Update, context: CallbackContext):
    global todayText
    todayText = 'Today is the day number {0} in the week number {1} in the year {2}'.format(
        day_of_year, week_of_year, year)
    update.message.reply_markdown_v2(todayText)
   
def schedule_command(update:Update, context:CallbackContext):
    user = update.message.from_user
    message = update.message.text.split(' ')
    time = message[1]
    hour = int(time[:2])
    minute = int(time[2:4])
    day = int(time[4:6])
    month = int(time[6:8])
    year = int(time[8:12])
    
    global date
    date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0)
    
    global note
    note = " ".join(message[2: :])
    strdate = str(date)
    
    update.message.reply_markdown_v2(f'Dear {user.mention_markdown_v2()} I will notify you on')




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler("today", today_command))
    dispatcher.add_handler(CommandHandler('schedule', schedule_command))
    # updater.dispatcher.add_handler(CommandHandler('notify', daily_job, pass_job_queue=True))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, start))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
