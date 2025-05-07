"""
Conversation-handler для команды /ai_assistant
(совместим с python-telegram-bot v20+)

Алгоритм:
1. /ai_assistant         → просим прислать *эталон* (пример/шаблон)
2. получаем эталон       → просим прислать *сырой* прайс-лист
3. получаем сырой прайс  → отправляем оба текста в GigaChat
   пока ждём — сообщение «⚙️ Обработка…»
4. присылаем пользователю готовый, отформатированный результат
"""

from __future__ import annotations

import asyncio
from enum import IntEnum
from typing import Final

from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
from telegram.helpers import escape

from gigachat_client import SYSTEM_PROMPT, chat_completion  # ← ваш клиент GigaChat

__all__ = ["register_ai_assistant"]

# ─────────────────────────── STATES ────────────────────────────
class AiStates(IntEnum):
    """Этапы работы ConversationHandler."""

    WAIT_TEMPLATE = 1  # ждём эталон-пример
    WAIT_RAW = 2  # ждём «сырой» прайс


# ─────────────────────────── HANDLERS ──────────────────────────
async def start_ai_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 1 — запрашиваем у пользователя эталон-пример."""

    raw_html = (
        "<b><u>🤖 AI-ассистент</u></b>\n\n"
        "Пришлите <b>два</b> сообщения:\n"
        "1. 📝 <u>Эталон</u> — как должен выглядеть <b>готовый</b> прайс-лист;\n"
        "2. 📄 <u>Сырой</u> прайс, который нужно отформатировать.\n\n"
        "Чтобы прервать диалог — /cancel 🚫"
    )
    await update.message.reply_html(raw_html)
    return AiStates.WAIT_TEMPLATE


async def receive_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 2 — сохраняем шаблон, просим «сырой» прайс."""

    context.user_data["ai_template"] = update.message.text
    await update.message.reply_html(
        "✨ <b><u>Отлично!</u></b> Теперь пришлите 📄 <b><u>сырой</u></b> прайс-лист, который нужно оформить."
    )
    return AiStates.WAIT_RAW


async def receive_raw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Шаг 3 — вызываем GigaChat, отправляем результат."""

    template: str | None = context.user_data.pop("ai_template", None)
    raw: str = update.message.text

    if not template:
        await update.message.reply_html("😕 Что-то пошло не так. Начните заново: /ai_assistant")
        return ConversationHandler.END

    # заглушка «Обработка…»
    processing = await update.message.reply_html("⚙️ <i>Обработка…</i>")

    messages = [
        SYSTEM_PROMPT,
        {"role": "user", "content": template},
        {"role": "user", "content": raw},
    ]

    try:
        formatted: str = await asyncio.to_thread(chat_completion, "GigaChat-Pro", messages)
        safe_text = escape(formatted)
        await processing.edit_text(safe_text, parse_mode="HTML")
    except Exception as exc:
        await processing.edit_text(
            f"❌ Ошибка при обращении к AI: {escape(str(exc))}\nПопробуйте позже.",
            parse_mode="HTML",
        )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """/cancel — досрочное завершение диалога."""

    context.user_data.pop("ai_template", None)
    await update.message.reply_html("🚫 <b>Операция отменена.</b>")
    return ConversationHandler.END


# ─────────────────────── REGISTRATION ──────────────────────────

def register_ai_assistant(application) -> None:
    """Регистрирует ConversationHandler в объекте application."""

    conv: Final = ConversationHandler(
        entry_points=[CommandHandler("ai_assistant", start_ai_assistant)],
        states={
            AiStates.WAIT_TEMPLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_template)],
            AiStates.WAIT_RAW: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_raw)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="ai_assistant_conversation",
        persistent=False,
    )
    application.add_handler(conv)