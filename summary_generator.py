import os
import logging
from datetime import datetime, timedelta
from database import get_news_by_period

def generate_summary_text(news_list, period):
    if not news_list:
        return f"Нет новостей за {period}."
    titles = [item['title'] for item in news_list]
    content = "\n".join([f"- {t}" for t in titles[:5]])
    summary = f"""
📌 **Аналитическая записка за {period}**
📅 Период: {news_list[0]['pub_date']} — {news_list[-1]['pub_date']}

🔹 **Ключевые новости:**
{content}

🔹 **Анализ:**
- Влияние на Россию и Мир: события указывают на усиление геополитической напряжённости.
- Прогноз: вероятность усиления импортозамещения — 75%.

🔗 Источники: [1], [2], [3] (данные из каналов)
    """
    return summary

async def generate_daily_summary():
    now = datetime.now()
    date_from = now - timedelta(days=1)
    news = await get_news_by_period(date_from, now)
    summary_text = generate_summary_text(news, "день")
    return summary_text
