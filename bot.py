import nest_asyncio
import asyncio

nest_asyncio.apply()

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes, ChatMemberHandler
import re

# Configuraciones
TOKEN = '7722269139:AAH_Uhmd3qE_rvr5HZP0cqyX_qKZK8suwwc'
PRIVATE_GROUP_USERNAME = '@teachdealsscrapelinks'   # Donde tú escribes los links
CHANNEL_USERNAME = '@blacktechdeals'                # Canal donde se envían
PUBLIC_GROUP_USERNAME = '@blacktechdealsgroup'      # Grupo público para bienvenidas
AFILIADO_TAG = 'blacktechdeal-20'                   # Tu Amazon Affiliate Tag

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('¡Hola! Soy tu bot 🤖')

# Dar bienvenida en grupo público
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        if update.chat_member.chat.username == PUBLIC_GROUP_USERNAME.replace('@', ''):
            await context.bot.send_message(
                chat_id=update.chat_member.chat.id,
                text=f"¡Bienvenido/a {member.full_name}! 🎉"
            )

# Limpiar y agregar tag de afiliado a links de Amazon
def limpiar_link_amazon(texto):
    match = re.search(r'(https?://(?:www\.)?amazon\.com\S*)', texto)
    if match:
        url = match.group(1)
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            asin = asin_match.group(1)
            return f"https://www.amazon.com/dp/{asin}?tag={AFILIADO_TAG}"
    return None  # Si no es un link de Amazon válido

# Reenviar, limpiar, agregar tag y borrar
async def forward_and_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_username = update.effective_chat.username

    if chat_username == PRIVATE_GROUP_USERNAME.replace('@', ''):
        if update.message and update.message.text:
            original_text = update.message.text
            link_limpio = limpiar_link_amazon(original_text)

            if link_limpio:
                # Si encuentra link de Amazon, manda el link limpio
                await context.bot.send_message(
                    chat_id=CHANNEL_USERNAME,
                    text=link_limpio
                )
            else:
                # Si no es link de Amazon, simplemente reenvía
                await context.bot.forward_message(
                    chat_id=CHANNEL_USERNAME,
                    from_chat_id=update.effective_chat.id,
                    message_id=update.message.message_id
                )

        # Borra el mensaje original
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )

# Función principal
async def main():
    print("Bot iniciado y funcionando 🚀")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_and_delete))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
