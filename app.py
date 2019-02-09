from telegram.ext import *
from telegram import InlineQueryResultArticle, InputTextMessageContent
import requests
import re

contents = requests.get('https://random.dog/woof.json').json()
image_url = contents['url']

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def bop(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    message = ' '.join(args).upper()
    chat_id = update.message.chat_id
    bot.send_message(chat_id, text=message)

def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def main():
    updater = Updater('714917830:AAFHnbU33XN3s0yE_sFxDM_AcfFJuUPkioI')
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler('caps', caps, pass_args=True))
    dp.add_handler(InlineQueryHandler(inline_caps))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
