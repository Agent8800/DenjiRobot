

import requests
from SaitamaRobot.events import register
from SaitamaRobot import telethn
from SaitamaRobot.__init__ import SUPPORT_CHAT
from bs4 import BeautifulSoup

@register(pattern='/watchorder')
async def watchorder(event):
	animename = event.message.message.replace(event.text.split(' ')[0], '')
	if len(animename) <= 1:
		await event.reply('/watchorder anime name')
		return
	try:
		res = requests.get(f'https://chiaki.site/?/tools/autocomplete_series&term={animename}').json()
		data = None
		id_ = res[0]['id']
		res_ = requests.get(f'https://chiaki.site/?/tools/watch_order/id/{id_}').text
		soup = BeautifulSoup(res_ , 'html.parser')
		anime_names = soup.find_all('span' , class_='wo_title')
		for x in anime_names:
			data = f"{data}\n{x.text}" if data else x.text
		await telethn.send_message(event.chat_id, f'Watchorder of <b>{animename}:</b> \n\n<tt>{data}</tt>',parse_mode='html', reply_to=event.id)
	except Exception as e:
		await event.reply(f'*Error*: Contact @{SUPPORT_CHAT}.\nERROR: {e}')
		return
