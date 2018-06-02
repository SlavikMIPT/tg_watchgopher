import datetime
import os
import shutil
from time import sleep

import telebot

import bottoken
import dbdump
import get_stats

bot = telebot.TeleBot(bottoken.release_token)
msg = bot.send_message('@MediaTube_chat', str(get_stats.get_io_child_count()))
bot.pin_chat_message('@MediaTube_chat', msg.message_id, disable_notification=True)


def main(argv):
    channel_id = int(argv[1])
    period_sec = int(argv[2])
    small_period_sec = 5
    counter = 0
    nload_pipe = get_stats.create_load_polling_thread()
    atop_pipe = get_stats.create_system_polling_thread()
    pin_str= ''
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
            ainc_load, aout_load = get_stats.get_channel_load(nload_pipe, r'Avg:')
            cinc_load, cout_load = get_stats.get_channel_load(nload_pipe, r'Curr:')
            cpu_load, free_ram = get_stats.get_system_load(atop_pipe)
            if counter / small_period_sec % 2 == 0:
                pre_str = '🌐↓↓*{0}{1}  * '.format(cinc_load[0],cinc_load[1])
            else:
                pre_str = '🌐↓  *{0}{1}  * '.format(cinc_load[0],cinc_load[1])
            if counter / small_period_sec / 2 % 2 == 0:
                pin_str = 'Σ:*{4}{5}*  👥 *SS5:{0}* *MTP:{3}* 🌡*CPU:{1}* *RAM:{2}*'.format(io_child_count, cpu_load, free_ram,
                                                                             io_mtproto,
                                                                             ainc_load[0], ainc_load[1])
            bot.edit_message_text(pre_str + pin_str, msg.chat.id, msg.message_id, parse_mode='Markdown')
            sleep(small_period_sec)
            counter += small_period_sec
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import sys

    main(sys.argv[0:])
