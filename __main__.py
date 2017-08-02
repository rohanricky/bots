import json
import requests
import time
from db import DB

db = DB()        # instance of DB class

TOKEN = "your_access_token_here"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def test_method():
    print("Text from bots.py")


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url = url + "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_id=[]
    for update in updates["result"]:
        update_id.append(int(update["update_id"]))
    return max(update_id)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def send_message(text, chat_id,reply_markup=None):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    if reply_markup:
        url+="&reply_markup={}".format(reply_markup)
    get_url(url)

def processing(text, chat):
    if text == "Rohan":
        text = "Hi Rohan, Fuck You!"
        send_message(text,chat)
    else:
        send_message(text,chat)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            processing(text, chat)
        except Exception as e:
            print(e)

def handle_updates(updates):
    for update in updates["result"]:
        try:
            text=update["message"]["text"]
            chat=update["message"]["chat"]["id"]
            items = db.items_list()

            if text == "/todo":
                message = "Add items to your todo list"
                send_message(message,chat)
                db.items_list()
                todo_updates(updates)

        except KeyError:
            pass

def todo_updates(updates):
    for update in updates["result"]:
        try:
            text=update["message"]["text"]
            chat=update["message"]["chat"]["id"]
            items = db.items_list()

            if text == "/todo":
                continue

            elif text in items:
                db.delete_item(text)
                items = db.items_list()

            elif text == "/done":
                keyboard=build_keyboard(items)
                send_message("Select an item to delete:",chat,keyboard)
                break

            else:
                db.add_item(text)
                items = db.items_list()
                message="\n".join(items)
                send_message(message,chat)

        except KeyError:
            pass


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
