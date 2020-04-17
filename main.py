import os
import shutil
import telebot
import bottoken
import dbdump

bot = telebot.TeleBot(bottoken.release_token)


def main(argv):
    channel_id = bottoken.CHANNEL_ID
    try:
        archive_path, dir_path = dbdump.create_dbdump()
        bot.send_document(channel_id, data=open(archive_path, 'rb'), disable_notification=True)
        os.remove(archive_path)
        shutil.rmtree(dir_path)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    import sys
    main(sys.argv[0:])
