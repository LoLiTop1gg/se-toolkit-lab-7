import sys
import asyncio
from handlers.commands import (
    handle_start, handle_help, handle_health,
    handle_labs, handle_scores, handle_unknown
)

async def handle_test(text: str) -> str:
    text = text.strip()
    if text == "/start":
        return await handle_start()
    elif text == "/help":
        return await handle_help()
    elif text == "/health":
        return await handle_health()
    elif text == "/labs":
        return await handle_labs()
    elif text.startswith("/scores"):
        parts = text.split(maxsplit=1)
        lab = parts[1] if len(parts) > 1 else ""
        return await handle_scores(lab)
    else:
        return await handle_unknown(text)

async def main():
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        if idx + 1 < len(sys.argv):
            command = sys.argv[idx + 1]
            response = await handle_test(command)
            print(response)
            sys.exit(0)
        else:
            print("Usage: uv run bot.py --test \"/command\"")
            sys.exit(1)
    else:
        from config import BOT_TOKEN
        from aiogram import Bot, Dispatcher
        from aiogram.filters import Command
        from aiogram.types import Message

        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()

        @dp.message(Command("start"))
        async def cmd_start(message: Message):
            await message.answer(await handle_start())

        @dp.message(Command("help"))
        async def cmd_help(message: Message):
            await message.answer(await handle_help())

        @dp.message(Command("health"))
        async def cmd_health(message: Message):
            await message.answer(await handle_health())

        @dp.message(Command("labs"))
        async def cmd_labs(message: Message):
            await message.answer(await handle_labs())

        @dp.message(Command("scores"))
        async def cmd_scores(message: Message):
            parts = message.text.split(maxsplit=1)
            lab = parts[1] if len(parts) > 1 else ""
            await message.answer(await handle_scores(lab))

        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
