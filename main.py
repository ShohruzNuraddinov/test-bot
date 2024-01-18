#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

from utils import random_jokes

FULL_NAME, PHONE_NUMBER = 1, 2


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f"Hi {user.mention_html()}\n FUll Name",
        parse_mode="HTML",
    )
    return FULL_NAME


def full_name(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Phone Number ", request_contact=True),
            ]
        ]
    )

    update.message.reply_text(
        "Phone Number",
        reply_markup=btn,
    )

    return PHONE_NUMBER


def phone_number(update: Update, context: CallbackContext) -> None:

    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Contact",),
            ],
            [
                KeyboardButton(text="Manzil", request_location=True),
            ],
            [
                KeyboardButton(text="Biz haqimizda",),
            ],
        ]
    )

    update.message.reply_text(
        "Home Page",
        reply_markup=btn,
    )

    return ConversationHandler.END


def random_command(update: Update, context: CallbackContext) -> None:
    random_jokes_text = random_jokes()
    update.message.reply_text(random_jokes_text)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5177104446:AAEJWX4QdWkPOsrjHV5MJOEN3GUFzs2k1Oo")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("random", random_command))

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FULL_NAME: [MessageHandler(Filters.text, full_name)],
            PHONE_NUMBER: [MessageHandler(Filters.contact, phone_number)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv)

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
