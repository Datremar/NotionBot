from telegram.ext import CommandHandler, Updater
from notion_client import Client

notion = Client(auth="your-token-goes-here")

def add_task(update, context):
    task = context.args[0]
    new_page = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": task
                    }
                }]
        }
    }
    database_id = "your-database-id-goes-here"
    notion.pages.create(parent={"database_id": database_id}, properties=new_page)
    update.message.reply_text(f"Task '{task}' added to Notion database!")

updater = Updater(token="your-telegram-bot-token-goes-here", use_context=True)
dispatcher = updater.dispatcher
add_task_handler = CommandHandler("add_task", add_task)
dispatcher.add_handler(add_task_handler)
updater.start_polling()