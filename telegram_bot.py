import logging

import telegram.constants
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


class ChatGPT3TelegramBot:
    def __init__(self, config, gpt3_bot):
        self.config = config
        self.gpt3_bot = gpt3_bot

    # Help menu
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("/start - Start the bot\n/reset - Reset conversation\n/help - Help menu")

    # Start the bot
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info('Bot started')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a Chat-GPT3 Bot, please talk to me!")

    # Reset the conversation
    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info('Resetting the conversation...')
        self.gpt3_bot.reset()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")

    # React to messages
    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info('New message received')
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.constants.ChatAction.TYPING)
        response = self.gpt3_bot.get_chat_response(update.message.text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response["message"],
            parse_mode=telegram.constants.ParseMode.MARKDOWN
        )
        logging.info('Sent response')

    def run(self):
        application = ApplicationBuilder().token(self.config['telegram_bot_token']).build()

        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CommandHandler('reset', self.reset))
        application.add_handler(CommandHandler('help', self.help))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt))

        application.run_polling()
