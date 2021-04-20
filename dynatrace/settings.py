import os

class Settings(object):
    bot_id = os.environ.get("MY_BOT_ID")
    bot_name = os.environ.get("MY_BOT_NAME")
    token = os.environ.get("MY_BOT_TOKEN")
    secret_phrase = os.environ.get("MY_SECRET_PHRASE")
    port = os.environ.get("MY_BOT_PORT")

    dyna_token=os.environ.get("DYNA_TOKEN")
