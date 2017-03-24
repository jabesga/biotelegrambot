from .basebot import BaseBot
import requests
import time
import re
import json
import sqlite3


class Bot(BaseBot):

    def __init__(self, token):
        super().__init__(token)


    def process_hook(self, response):
        if 'message' in response:            
            if 'text' in response['message']:
                if response['message']['text'] == '/start': # or response['message']['text'] == '/rules@IdePyBot':
                    json_response = self.send_message(response['message']['from']['id'],
                                      parse_mode='HTML', disable_web_page_preview=True, text=self.pinned_message)
                    print(json_response)

        if 'inline_query' in response:
            pass

    def process_response(self):

        response = self.process_updates()

        if not response:
            return
        if not 'inline_query' in response:
            return
        if response['inline_query']['query']:
            user = response['inline_query']['query']
            print(user)

            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute("SELECT * FROM tg_users WHERE username='%s'" % user)
            description = c.fetchone()
            if not description:
                return
            print(description[1])

            document = json.dumps([{'type': 'article',
                                        'id': '0',
                                        'input_message_content': {'message_text': 'Bio of @%s: %s' % (user, description[1]) },
                                        'title': 'Bio of {}'.format(user),
                                        'description': description[1],
                                        'thumb_url': '',
                                        'thumb_width': 512,
                                        'thumb_height': 512}])

            json_response = requests.post(
                url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'answerInlineQuery'),
                data={'inline_query_id': response['inline_query']['id'], 'results': document}
            ).json()

        return response