import os

class Settings(object):
    bot_id = os.environ.get("MY_BOT_ID")
    bot_name = os.environ.get("MY_BOT_NAME")
    token = os.environ.get("MY_BOT_TOKEN")
    secret_phrase = os.environ.get("MY_SECRET_PHRASE")
    port = os.environ.get("MY_BOT_PORT")

    dd_api_key=os.environ.get("DD_API_KEY")
    dd_application_key=os.environ.get("DD_APPLICATION_KEY")
    dd_creator_id=os.environ.get("DD_CREATOR_ID")
