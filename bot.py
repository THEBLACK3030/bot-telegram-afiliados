from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ChatMemberHandler, filters
import nest_asyncio
import asyncio

nest_asyncio.apply()

TOKEN = '7722269139:AAG4yryGIrygmh8vY-ByXlL_TaypE9tRxL0'
PRIVATE_GROUP_USERNAME = '@teachdealsscrapelinks'
CHANNEL_USERNAME = '@blacktechdeals'
PUBLIC_GROUP_USERNAME = '@blacktechdealsgroup'

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('¡Hola! Soy el bot 🤖')

# Bienvenida personalizada con botones
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        if update.chat_member.chat.username == PUBLIC_GROUP_USERNAME.replace('@', ''):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Canal de Ofertas", url="https://t.me/blacktechdeals")],
                [InlineKeyboardButton("💬 Grupo de Chat", url="https://t.me/blacktechdealsgroup")]
            ])
            await context.bot.send_message(
                chat_id=update.chat_member.chat.id,
                text=f"👋 ¡Bienvenido/a, {member.full_name}!\n\n"
                     "🚀 Este es *BlackTechDeals Group*, donde la tecnología y las gangas se encuentran.\n"
                     "🎯 Aquí cazamos ofertas *antes que nadie*.\n\n"
                     "🔗 *Accede rápido:*",
                parse_mode='Markdown',
                reply_markup=keyboard
            )

# Reenviar mensaje y borrar
async def forward_and_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_username = update.effective_chat.username
    if chat_username == PRIVATE_GROUP_USERNAME.replace('@', ''):
        await context.bot.forward_message(
            chat_id=CHANNEL_USERNAME,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )

async def main():
    print("Bot iniciado 🚀")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_and_delete))

    await app.run_polling()

if name == '__main__':
    asyncio.run(main())