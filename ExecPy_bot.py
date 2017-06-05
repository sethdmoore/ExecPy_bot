#!/usr/bin/env python3
from subprocess import Popen, PIPE
import os
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

class ExecPyBot(object):
    def __init__(self, token=None, authorized_users=[]):
        if token is None:
            token = os.getenv("EXECPY_API_TOKEN")

        if len(authorized_users) == 0:
            auth_str = os.getenv("EXECPY_AUTHORIZED_USERS")
            authorized_users = auth_str.split(":")
            if not auth_str:
                print("No authorized users defined")
                raise ValueError

        self.authorized_users = authorized_users
        self.temp_file = "/tmp/ex.py"
        self.python_bin = "python3"

        if token:
            self.token = token
        else:
            print("No token defined")
            print("(EG, EXECPY_API_TOKEN) or ExecPyBot('SOMETOKEN')")
            raise ValueError

        self.canned_msgs = {
           "greeting": "Python3 Eval Bot Started",
           "unauthorized": "You are not authorized to use this bot."
        }

        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()


    def eval_handler(self, bot, update):
        msg = update.message
        txt = msg.text
        uid = update.message.from_user.id

        if str(uid) not in self.authorized_users:
            bot.send_message(chat_id=msg.chat_id, text=self.canned_msgs["unauthorized"])
            return

        eval_list = []

        logging.info(txt)
        logging.info(msg)
        # logging.info(txt)

        if msg.entities:
            for e in msg.entities:
                print(e)
                if e.type == "pre":
                    # convert an object to a dictionary
                    eval_list.append({# "type": e.type,
                                      "offset": e.offset,
                                      "length": e.length})

        for script in eval_list:
            # slice the text into groups of strings correctly
            offset, length = script["offset"], script["length"]
            snippet=txt[offset:offset + length]
            output = self.exec_command(snippet)
            bot.send_message(chat_id=msg.chat_id, text=output)


    def add_handlers(self):
        # set up command / message handling
        eval_handler = MessageHandler(Filters.text, self.eval_handler)
        start_handler = CommandHandler('start', self.start_cmd)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(eval_handler)

        logging.info("started")


    def exec_command(self, script):
        with open(self.temp_file, 'w') as f:
            f.write(script)
        p = Popen([self.python_bin, self.temp_file], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        out, err = p.communicate()
        output = "%s%s\n" % (out, err)
        return output


    def run(self):
        self.updater.start_polling()


    def inline_caps(bot, update):
        query = update.inline_query.query
        if not query:
            return


    def start_cmd(self, bot, update):
        logging.info(update.message)
        logging.info(update.message.from_user.id)
        bot.send_message(chat_id=update.message.chat_id, text="Python3 Eval Bot Started")


def main():
    b = ExecPyBot()
    b.run()


if __name__ == '__main__':
    main()
