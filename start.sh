#!/bin/bash

# نصب ffmpeg
apt-get update && apt-get install -y ffmpeg

# اجرای دستورهای اصلی
gunicorn app:app & python3 bot.py
