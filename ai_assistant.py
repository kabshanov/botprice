"""
Conversation-handler для команды /ai_assistant
(работает с python-telegram-bot v20+)

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
from telegram.helpers import escape_markdown
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

from gigachat_client import SYSTEM_PROMPT, chat_completion   # ← ваш клиент GigaChat


# ─────────────────────────── STATES ────────────────────────────
class AiStates(IntEnum):
    WAIT_TEMPLATE = 1     # ждём эталон-пример
    WAIT_RAW      = 2     # ждём «сырой» прайс


# ─────────────────────────── HANDLERS ──────────────────────────
async def start_ai_assistant(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Шаг 1 — запрашиваем у пользователя эталон-пример."""
    raw = (
        "*AI-ассистент*\n\n"
        "Пришлите *два* сообщения:\n"
        "1\\. _Эталон_ — как должен выглядеть **готовый** прайс-лист;\n"
        "2\\. _Сырой_ прайс, который нужно отформатировать.\n\n"
        "Чтобы прервать диалог — /cancel"
    )
    await update.message.reply_markdown_v2(
        escape_markdown(raw, version=2)
    )
    return AiStates.WAIT_TEMPLATE


async def receive_template(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Шаг 2 — сохраняем шаблон, просим сырой прайс."""
    context.user_data["ai_template"] = update.message.text
    await update.message.reply_markdown(
        "_Отлично! Теперь пришлите **сырой** прайс-лист, который нужно оформить._"
    )
    return AiStates.WAIT_RAW


async def receive_raw(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Шаг 3 — вызываем GigaChat и отправляем результат."""
    template: str | None = context.user_data.pop("ai_template", None)
    raw: str = update.message.text

    if not template:
        await update.message.reply_text(
            "😕 Что-то пошло не так. Начните заново: /ai_assistant"
        )
        return ConversationHandler.END

    # заглушка «обработка…»
    processing = await update.message.reply_text("⚙️ Обработка…")

    # формируем prompt для GigaChat
    messages = [
        SYSTEM_PROMPT,                    # системный промпт из gigachat_client.py
        {"role": "user", "content": template},
        {"role": "user", "content": raw},
    ]

    try:
        # чтобы не блокировать event-loop, зовём ИИ в отдельном потоке
        formatted = await asyncio.to_thread(
            chat_completion, "GigaChat-Pro", messages
        )

        await processing.edit_text(
            formatted, parse_mode="Markdown"
        )
    except Exception as e:
        await processing.edit_text(
            f"❌ Ошибка при обращении к AI: {e}\nПопробуйте позже."
        )

    return ConversationHandler.END


async def cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """/cancel — досрочное завершение диалога."""
    context.user_data.pop("ai_template", None)
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END


# ─────────────────────── REGISTRATION ──────────────────────────
def register_ai_assistant(application) -> None:
    """
    Регистрирует ConversationHandler внутри объекта `application`
    (Application из python-telegram-bot).
    """
    conv: Final = ConversationHandler(
        entry_points=[CommandHandler("ai_assistant", start_ai_assistant)],
        states={
            AiStates.WAIT_TEMPLATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_template)
            ],
            AiStates.WAIT_RAW: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_raw)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="ai_assistant_conversation",
        persistent=False,
    )
    application.add_handler(conv)
