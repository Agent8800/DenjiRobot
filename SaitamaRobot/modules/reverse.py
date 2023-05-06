import requests
import json
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler

from MitsuriRobot import dispatcher


url = 'https://google-reverse-image-api.vercel.app/reverse'

def reverse(update, context):
    message = update.effective_message
    chat_id = update.effective_chat.id

    reply = message.reply_to_message

    if reply:
        if reply.sticker:
            file_id = reply.sticker.file_id
            new_id = reply.sticker.file_unique_id
        elif reply.photo:
            file_id = reply.photo[-1].file_id
            new_id = reply.photo[-1].file_unique_id
        else:
            message.reply_text("Reply To An Image Or Sticker To Lookup!")
            return 
            
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
