import os
import shutil
from time import sleep

import telebot

import bottoken
import dbdump
import get_stats
import datetime
bot = telebot.TeleBot(bottoken.release_token)
msg = bot.send_message('@MediaTube_chat', str(get_stats.get_io_child_count()))
bot.pin_chat_message('@MediaTube_chat', msg.message_id, disable_notification=True)


def main(argv):
    channel_id = int(argv[1])
    period_sec = int(argv[2])
    small_period_sec = 30
    counter = 0
    while True:
        try:
            date_str = str(datetime.datetime.now().strftime('%d.%m'))
            time_str = str(datetime.datetime.now().strftime('%H:%M'))
            if counter >= period_sec:
                archive_path, dir_path = dbdump.create_dbdump()
                bot.send_document(channel_id, data=open(archive_path, 'rb'), disable_notification=True)
                os.remove(archive_path)
                shutil.rmtree(dir_path)
                counter = 0
            io_child_count = get_stats.get_io_child_count()
            io_mtproto = get_stats.get_mtproto_connections()
            bot.edit_message_text('🌐 *ss5:{0} mtp:{3}*  *{2}* {1}'.format(io_child_count, date_str, time_str, io_mtproto),
                                  msg.chat.id, msg.message_id, parse_mode='Markdown')
            sleep(small_period_sec)
            counter += small_period_sec
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import sys

    main(sys.argv[0:])
