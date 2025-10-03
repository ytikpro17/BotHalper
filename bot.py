from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8447378243:AAGrnR8JanQWCekgkz6INhIf8vCkOPPhawc"
ADMIN_ID = 7235298645

users = {}

main_menu = ReplyKeyboardMarkup(
    [["Мій профіль", "Налаштування"],
     ["Сайт", "Допомога"],
     ["Надіслати ідею"]],
    resize_keyboard=True
)

settings_menu = ReplyKeyboardMarkup(
    [["Змінити ім’я"], ["Назад у меню"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = update.effective_user.first_name
    await update.message.reply_text(f"Привіт, {users[user_id]}! 👋\nОберіть дію нижче:", reply_markup=main_menu)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if text == "Мій профіль":
        await update.message.reply_text(f"🧑 Ім'я: {users[user_id]}\nID: {user_id}")
    elif text == "Налаштування":
        await update.message.reply_text("⚙️ Налаштування:", reply_markup=settings_menu)
    elif text == "Змінити ім’я":
        await update.message.reply_text("Введіть нове ім'я:")
        context.user_data["awaiting_name"] = True
    elif text == "Назад у меню":
        await update.message.reply_text("⬅️ Повертаємось у меню.", reply_markup=main_menu)
    elif text == "Сайт":
        await update.message.reply_text("🌐 Сайт: https://ytikpro17.github.io/My_Site/")
    elif text == "Допомога":
        await update.message.reply_text(
            "📖 YtikPost\nЦе моя особиста сторінка, де я ділюся проєктами, ідеями та творчістю.\n"
            "Тут можна знайти інформацію про мене, переглянути галерею зображень і дізнатися про нові оновлення."
        )
    elif text == "Надіслати ідею":
        await update.message.reply_text("💡 Введіть вашу ідею:")
        context.user_data["awaiting_idea"] = True
    else:
        if context.user_data.get("awaiting_name"):
            users[user_id] = text
            context.user_data["awaiting_name"] = False
            await update.message.reply_text(f"✅ Ім'я змінено на: {text}", reply_markup=main_menu)
        elif context.user_data.get("awaiting_idea"):
            context.user_data["awaiting_idea"] = False
            await update.message.reply_text("✅ Дякуємо! Ідея надіслана адміну.", reply_markup=main_menu)
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"💡 Нова ідея від {users.get(user_id,'Невідомий')} (ID {user_id}):\n{text}")
        else:
            await update.message.reply_text("Не розпізнано. Спробуйте /start.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
