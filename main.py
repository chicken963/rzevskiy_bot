import csv

import yaml
from telegram.ext import MessageHandler, filters, Application

import re
import logging

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
    encoding='utf-8',
    level=logging.INFO)


def read_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)


async def message_handler(update, context):
    text = update.message.text
    logging.info(text)
    pattern_with_optinal_punctuation = "{}([!?.,;:\"'])*$"

    with open('triggers_and_replies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            trigger = row[0]
            pattern = pattern_with_optinal_punctuation.format(trigger)
            if re.match(pattern, text, re.IGNORECASE):
                reply = row[1]
                await update.message.reply_text(text=reply, quote=True)


def main():
    config_map = read_config()
    api_token = config_map['telegram']['api-key']
    dp = Application.builder().token(api_token).build()
    dp.add_handler(MessageHandler(filters.TEXT, message_handler))
    dp.run_polling()


if __name__ == '__main__':
    main()
