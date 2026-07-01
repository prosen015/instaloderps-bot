import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, START_MESSAGE
from downloader import download_instagram


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "instagram.com" not in text:
        await update.message.reply_text(
            "❌ Please send a valid public Instagram Reel or Post link."
        )
        return

    msg = await update.message.reply_text("⏳ Downloading...")

    try:
        file_path = download_instagram(text)

        if not file_path:
            await msg.edit_text("❌ Download failed.")
            return

        if file_path.lower().endswith((".mp4", ".mov", ".mkv", ".webm")):
            with open(file_path, "rb") as video:
                await update.message.reply_video(video=video)
        else:
            with open(file_path, "rb") as photo:
                await update.message.reply_photo(photo=photo)

        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
