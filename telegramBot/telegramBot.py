#!/usr/bin/env python
# -*- coding:utf-8 -*-

from telegram.ext import MessageHandler, Filters, Updater
from telegram import *
from utils.timelog import TimeLogger
import logging
import requests
import time
import traceback
from concurrent import futures
from datetime import datetime, timedelta
from telegram.ext import CommandHandler
proxies = {
    'https': 'https://127.0.0.1:50861',
    'http': 'http://127.0.0.1:50861',
}

logger = TimeLogger('telegram_trainPass_monitor%s.log' % time.strftime('%Y-%m-%d'))
myselfBot = ''


class TelegramBot:
    def __init__(self):
        self.bot = Bot(myselfBot)

    def start(self, update):
        self.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

    def reply(self):
        updater = Updater(token=myselfBot)
        dispatcher = updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        #dispatcher.add_handler(MessageHandler(Filters.text, self.monitor_pnl))
        updater.start_polling()
        updater.idle()

def main():
    myBot = TelegramBot()
    myBot.reply()

if __name__ == '__main__':
    main()
