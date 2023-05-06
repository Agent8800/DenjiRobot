import requests
import json
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler

from MitsuriRobot import dispatcher, bot_token as token


url = 'https://google-reverse-image-api.vercel.app/reverse'

def reverse(update: Update, context: CallbackContext):
    if not update.effective_message.reply_to_message:
        update.effective_message.reply_text("Reply to a photo.")

    elif not update.effective_message.reply_to_message.photo:
        update.effective_message.reply_text("Reply to an image.")
            
       elif update.effective_message.reply_to_message.photo:
        msg = update.effective_message.reply_text("Searching.....")

        photo_id = update.effective_message.reply_to_message.photo[-1].file_id
        get_path = requests.post(
            f"https://api.telegram.org/bot{Token}/getFile?file_id={photo_id}"
        ).json()
        file_path = get_path["result"]["file_path"]
        data = {
            "imageUrl": f"https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url=https://api.telegram.org/file/bot{Token}/{file_path}"
        }

        response = requests.post(url, json=data)
        result = response.json()
        if response.ok:
            msg.edit_text(
                f"[{result['data']['resultText']}]({result['data']['similarUrl']})",
                parse_mode=ParseMode.MARKDOWN,
   reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Check this out", url="https://t.me/tyranteyeeee/36603"
                            )a
                        ]
                    ]
                ),
            )
        else:
            update.effective_message.reply_text("Some exception occured")

dispatcher.add_handler(CommandHandler(["pp", "grs", "p", "reverse"], reverse))
