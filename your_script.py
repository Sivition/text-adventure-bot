import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7035638590:AAFO2C_iToTiDlRfrilLeT_9CIv-oSJGFis'
IMAGES_DIR = 'images'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Добро пожаловать в Текстовое приключение!')
    await show_screen(update, context, 'start')

async def show_screen(update: Update, context: ContextTypes.DEFAULT_TYPE, screen):
    text, choices, image_filename = "", [], ""
    
    if screen == 'start':
        text = "Вы наконец-то собрали яйца в кулак и решили пойти в лес за дровами."
        choices = [("Ну, я пошёл", "forest"), ("Сходить в деревню", "village")]
        image_filename = 'start.png'
    elif screen == 'forest':
        text = "Вы вошли в лес. Здесь темно и страшно, вы чувствуете как живот предательски урчит. Хорошо, что ещё не стемнело."
        choices = [("дрова сами себя не соберут", "deep_forest"), ("думаю стоит вернутся", "end")]
        image_filename = 'forest.png'
    elif screen == 'village':
        text = "Вы пришли в деревню. Дома старые и унылые. Недалеко старый дед ссыт на забор."
        choices = [("Поговорить с дедом", "talk"), ("Вернуться к лесу", "start")]
        image_filename = 'village.png'
    
    keyboard = [[InlineKeyboardButton(choice[0], callback_data=choice[1])] for choice in choices]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    
    if image_filename:
        await show_image(update, context, image_filename)

async def show_image(update: Update, context: ContextTypes.DEFAULT_TYPE, image_filename):
    image_path = os.path.join(IMAGES_DIR, image_filename)
    if os.path.isfile(image_path):
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'))
    else:
        logger.error(f"Файл не найден: {image_path}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_screen(query, context, query.data)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
