import csv
import io
import random

import yaml
from telegram.ext import MessageHandler, filters, Application

import re
import logging

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
    encoding='utf-8',
    level=logging.ERROR)


def read_config():
    with io.open('config.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


config_map = read_config()
replies = 0


def choose_any(row):
    available_replies = row[1:]
    return random.choice(available_replies)


async def process_full_message_triggers(message):
    text = message.text
    pattern_with_optional_punctuation = "{}([!?.,;:\"'])*$"
    with open('triggers_and_replies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            trigger = row[0]
            pattern = pattern_with_optional_punctuation.format(trigger)
            if re.match(pattern, text, re.IGNORECASE):
                reply = choose_any(row)
                global replies
                replies += 1
                await message.reply_text(text=reply, quote=True)


async def process_snippet_message_triggers(message):
    text = message.text
    with open('trigger_words.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            trigger = row[0]
            if re.search(trigger, text, re.IGNORECASE):
                reply = row[1]
                global replies
                replies += 1
                await message.reply_text(text=reply, quote=True)


async def reply_to_sanya(message):
    sanya_pattern_eng = "(^Ale(x|ks)and(e?r$|ro)$)|(^San(dro|[yi]a|[yi]ok)$)|(^Sash(k?a|ok)$)|(^Shur(a|ic*k)$)"
    sanya_pattern_rus = "(^Александр$)|(^Саш[ау].*)|(^Сан(я([гр]а)*|[её]к)$)|(^Шур(а|ик)$)"
    message_sender_name = message.from_user.first_name
    if re.match(sanya_pattern_eng, message_sender_name, re.IGNORECASE) or re.match(sanya_pattern_rus,
                                                                                   message_sender_name, re.IGNORECASE):
        await message.reply_voice("sanya.mp3", quote=True)


async def reply_to_kirill(message, context):
    message_sender_name = message.from_user.first_name
    if re.search("Kirill", message_sender_name, re.IGNORECASE) and random.randint(1, 20) == 1:
        global config_map
        await context.bot.send_message(message.chat_id, config_map['replies']['kirill'])
        await context.bot.send_sticker(message.chat_id, random.choice(config_map['stickers']['gachi']))


async def message_handler(update, context):
    message = update.message
    global replies
    replies = 0
    await process_full_message_triggers(message)
    await process_snippet_message_triggers(message)
    if replies == 0 and random.randint(1, 100) == 1:
        await reply_to_sanya(message)
    await reply_to_kirill(message, context)


def main():
    api_token = config_map['telegram']['api-key']
    dp = Application.builder().token(api_token).build()
    dp.add_handler(MessageHandler(filters.TEXT, message_handler))
    dp.run_polling()


if __name__ == '__main__':
    main()
