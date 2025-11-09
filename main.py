import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from summary_generator import generate_daily_summary

# 🔐 Секреты ТОЛЬКО через переменные окружения — НИКАКИХ .env
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Проверка обязательных переменных
if not BOT_TOKEN:
    logging.critical("❌ TELEGRAM_BOT_TOKEN не задан в окружении!")
    raise EnvironmentError("Telegram bot token not set!")

if not ADMIN_CHAT_ID:
    logging.critical("❌ ADMIN_CHAT_ID не задан в окружении!")
    raise EnvironmentError("Admin chat ID not set!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🤖 Бот запущен. Он анализирует новости и формирует отчёты.")

# Команда для тестирования
@dp.message(Command("send_daily"))
async def cmd_send_daily(message: types.Message):
    summary = await generate_daily_summary()
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary, parse_mode="Markdown")

# Эндпоинт для cron-job.org
from fastapi import FastAPI
from contextlib import asynccontextmanager

app = FastAPI()

@app.get("/trigger_daily")
async def trigger_daily():
    summary = await generate_daily_summary()
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary, parse_mode="Markdown")
    return {"status": "sent"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(dp.start_polling(bot))
    yield
    await bot.session.close()
    task.cancel()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, lifespan="on")
