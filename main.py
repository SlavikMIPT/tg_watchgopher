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
    small_period_sec = 1.5
    counter = 0
    nload_pipe = get_stats.create_load_polling_thread()
    atop_pipe = get_stats.create_system_polling_thread()
    pin_str = ''
    earth_emoji = ['🌎', '🌍', '🌏']
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
            if int(counter) % 2 == 0:
                pre_str = '🌐↓↓*{0: <3}{1}  * '.format(cinc_load[0],cinc_load[1])
            else:
                pre_str = '🌐↓  *{0: <3}{1}  * '.format(cinc_load[0],cinc_load[1])
            if int(counter)/2 % 2 == 0:
                pin_str = '↓Σ*{4: <3}{5}*  👥*SS5:{0: <4}* *MTP:{3: <4}* 🌡*CPU:{1: <3}* *RAM:{2: <5}*'.format(io_child_count, cpu_load, free_ram,
                                                                             io_mtproto,
                                                                             ainc_load[0], ainc_load[1])
            bot.edit_message_text(pre_str + pin_str, msg.chat.id, msg.message_id, parse_mode='Markdown')
            # pre_str = earth_emoji[int(counter) % 3]
            # if int(counter) % 2 == 0:
            #     pin_str = '🌐️↓*{0: <3}{1}* 👥*SS5:{2: <4}*🔸*CPU:{3: <4}*  ↓Σ:*{4}{5}*'.format(cinc_load[0], cinc_load[1], io_child_count,
            #                                                              cpu_load,ainc_load[0], ainc_load[1])
            # else:
            #     pin_str = '🌐️↓*{0: <3}{1}* 👥*MTP:{2: <4}*🔹*RAM:{3: <4}*  ↓Σ:*{4}{5}*'.format(cinc_load[0], cinc_load[1], io_mtproto,
            #                                                              free_ram,ainc_load[0], ainc_load[1])


            sleep(small_period_sec)
            counter += 1
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import sys

    main(sys.argv[0:])
