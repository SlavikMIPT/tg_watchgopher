import os
import shutil
from time import sleep

import telebot

import bottoken
import dbdump

bot = telebot.TeleBot(bottoken.release_token)


def main(argv):
    channel_id = int(argv[1])
    period_sec = int(argv[2])
    while True:
        archive_path, dir_path = dbdump.create_dbdump()
        bot.send_document(channel_id, data=open(archive_path, 'rb'), disable_notification=True)
        os.remove(archive_path)
        shutil.rmtree(dir_path)
        sleep(period_sec)


if __name__ == '__main__':
    import sys

    main(sys.argv[0:])
