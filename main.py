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
    small_period_sec = 1
    counter = 0
    nload_pipe = get_stats.create_load_polling_thread()
    atop_pipe = get_stats.create_system_polling_thread()
    pin_str = ''
    earth_emoji = ['🌎', '🌍', '🌏']
    tg_err_flag = '🔹'
    err_down = 0
    while True:
        try:
            # date_str = str(datetime.datetime.now().strftime('%d.%m'))
            # time_str = str(datetime.datetime.now().strftime('%H:%M'))
            if counter >= period_sec:
                archive_path, dir_path = dbdump.create_dbdump()
                bot.send_document(channel_id, data=open(archive_path, 'rb'), disable_notification=True)
                os.remove(archive_path)
                shutil.rmtree(dir_path)
                counter = 0
            io_child_count = get_stats.get_io_child_count()
            io_mtproto = get_stats.get_mtproto_connections()
            ainc_load, aout_load = get_stats.get_channel_load(nload_pipe, r'Avg:')
            if int(counter) % 600 == 0:
                err_down = get_stats.get_downdetector_stats()
                tg_err_flag = '🔹'
                if err_down in range(10, 20):
                    tg_err_flag = '🔸'
                elif err_down >= 20:
                    tg_err_flag = '♦️'
            # cinc_load, cout_load = get_stats.get_channel_load(nload_pipe, r'Curr:')
            cpu_load, free_ram = get_stats.get_system_load(atop_pipe)  # 🔹🔸️
            if int(counter) % 2 == 0:
                pin_str = '👥*SCK:{0}k 🔰MTP:{1} {5}ERR:{4}   🌡CPU:{2}  RAM:{3} 🔹*'.format(
                    float(int(io_child_count / 100)) / 10,
                    int(io_mtproto),
                    cpu_load, free_ram, err_down, tg_err_flag)
            else:
                pin_str = '👥*SCK:{0}k 🔰MTP:{1} {5}ERR:{4}   🌡CPU:{2}  RAM:{3}  *'.format(
                    float(int(io_child_count / 100)) / 10,
                    int(io_mtproto),
                    cpu_load, free_ram, err_down, tg_err_flag)
            pre_str = '🔻🔺*|{0}{1}|{2}{3}|*   '.format(ainc_load[0], ainc_load[1], aout_load[0], aout_load[1])

            bot.edit_message_text(pre_str + pin_str, msg.chat.id, msg.message_id, parse_mode='Markdown')

            sleep(small_period_sec)
            counter += small_period_sec
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import sys

    main(sys.argv[0:])
