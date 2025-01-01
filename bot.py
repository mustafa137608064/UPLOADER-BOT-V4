import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
from plugins.config import Config

from pyrogram import Client as Ntbots
from pyrogram import filters
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":

    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="plugins")
    Ntbots = Ntbots(
        "URL UPLOADER BOT",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins)

    print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
    Ntbots.run()


@Ntbots.on_message(filters.private & filters.document)
async def handle_document(client, message):
    # Allowed file extensions
    allowed_extensions = [".zip", ".apk", ".exe", ".rar"]

    # Extract file name and extension
    file_name = message.document.file_name
    file_extension = os.path.splitext(file_name)[1].lower()

    if file_extension in allowed_extensions:
        await message.reply_text(f"✅ File '{file_name}' is accepted and will be uploaded.")
        # Proceed with downloading and processing the file
        file_path = await message.download()
        await message.reply_document(document=file_path)
        os.remove(file_path)
    else:
        await message.reply_text(f"❌ File '{file_name}' is not supported. Allowed formats: {', '.join(allowed_extensions)}.")
