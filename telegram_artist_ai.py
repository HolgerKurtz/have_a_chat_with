import json
import logging
import os
import html
import traceback
from functools import wraps
from dotenv import load_dotenv

from telegram import Bot, ChatAction, Update, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackContext
from better_profanity import profanity

import AIimage

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


with open('telegram_creds.json', "r") as json_file:
    telegram_creds = json.load(json_file)

TOKEN = os.getenv("Token")
DEVELOPER_CHAT_ID = os.getenv("DEVELOPER_CHAT_ID")

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

profanity.load_censor_words()

""" BASIC TELEGRAM BOT STUFF """


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func

    return decorator


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID,
                             text=message, parse_mode=ParseMode.HTML)
dispatcher.add_error_handler(error_handler)


def start(update, context):
    update.message.reply_text("Wuff")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def ai_image(update, context):
    update.message.reply_text("Wuff")
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

@send_action(ChatAction.TYPING)
def wuff(update, context):
    update.message.reply_text("Wuff")
wuff_handler = MessageHandler(Filters.text & (~Filters.command), wuff)
dispatcher.add_handler(wuff_handler)


def unknown(update, context):
    # Handle the unknown 👀
    update.message.reply_text("Wuff?")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

if __name__ == "__main__":
    # Starting the bot
    # For stopping the bot press: ctrl + c
    updater.start_polling()
    updater.idle()
