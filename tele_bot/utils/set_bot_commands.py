from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Добавить заявку"),
            types.BotCommand("end", "Добавить заявку"),
            types.BotCommand("reset", "Сбросить текущую заявку"),
        ]
    )
