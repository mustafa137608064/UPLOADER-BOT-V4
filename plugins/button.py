import asyncio
import json
import math
import os
import shutil
import time
import subprocess
from datetime import datetime
from pyrogram import enums
from plugins.config import Config
from plugins.script import Translation
from plugins.thumbnail import *
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes
from plugins.database.database import db
from PIL import Image
from plugins.functions.ran_text import random_char

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def check_ffmpeg_installed():
    """Check if ffmpeg is installed on the system."""
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def get_buttons():
    """Generate the buttons for download type selection."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("DEFAULT", callback_data="download_default")],
        ]
    )

async def youtube_dl_call_back(bot, update):
    """Callback for processing YouTube downloads."""
    cb_data = update.data
    tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split("|")
    
    if tg_send_type == "download_default":
        await process_default_download(bot, update)
    else:
        await update.message.edit_caption("Invalid download type selected.")

async def process_default_download(bot, update):
    """Process download and upload as-is (default)."""
    if not check_ffmpeg_installed():
        await update.message.edit_caption(
            caption="Error: ffmpeg is not installed. Please install ffmpeg to download files."
        )
        return False

    # Extract file details
    cb_data = update.data
    tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split("|")
    youtube_dl_url = update.message.reply_to_message.text

    # Use yt-dlp to download the file
    random1 = random_char(5)
    tmp_directory_for_each_user = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}{random1}")
    os.makedirs(tmp_directory_for_each_user, exist_ok=True)

    custom_file_name = f"{random_char(10)}.{youtube_dl_ext}"
    download_directory = os.path.join(tmp_directory_for_each_user, custom_file_name)

    command_to_exec = [
        "yt-dlp",
        "--no-mtime",
        "-f", youtube_dl_format,
        youtube_dl_url,
        "-o", download_directory
    ]

    # Execute the download command
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()

    if process.returncode != 0:
        await update.message.edit_caption(f"Error during download: {e_response}")
        return False

    # Upload the downloaded file
    await update.message.reply_document(
        document=download_directory,
        caption=f"Here is your file: {custom_file_name}"
    )

    # Clean up
    shutil.rmtree(tmp_directory_for_each_user)
