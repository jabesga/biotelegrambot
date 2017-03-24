from flask import Flask, request
from .bot import Bot
import os
import time

app = Flask(__name__)
app.debug = True

TOKEN = os.environ['token']
try:
    HEROKU_APP = os.environ['app_url']
except KeyError:
    HEROKU_APP = None

# Create bot object and set webhook
bot = Bot(TOKEN)

if HEROKU_APP:
    json_response = bot.set_webhook(HEROKU_APP + '/{0}'.format(TOKEN))

    @app.route("/{0}".format(TOKEN), methods=['POST'])
    def hook():
        bot.process_hook(request.get_json())
        return '', 200
else:
    while True:
        print(bot.process_response())
        time.sleep(2)



