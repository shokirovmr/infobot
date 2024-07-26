from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from django.core.management.base import BaseCommand

from apps.infobot.models import CompanyInfo, Partner, Investor

API_TOKEN = "YOUR_TELEGRAM_BOT_API_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_paginated_keyboard(model, page=1):
    items_per_page = 5
    total_items = model.objects.count()
    total_pages = (total_items + items_per_page - 1) // items_per_page
    items = model.objects.all()[(page - 1) * items_per_page : page * items_per_page]

    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in items:
        keyboard.add(
            InlineKeyboardButton(
                item.name, callback_data=f"{model.__name__}_detail_{item.id}"
            )
        )

    if page > 1:
        keyboard.add(
            InlineKeyboardButton(
                "⬅️ Previous", callback_data=f"{model.__name__}_page_{page - 1}"
            )
        )
    if page < total_pages:
        keyboard.add(
            InlineKeyboardButton(
                "Next ➡️", callback_data=f"{model.__name__}_page_{page + 1}"
            )
        )

    return keyboard


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Company Info", callback_data="company_info"))
    keyboard.add(InlineKeyboardButton("Services", callback_data="services"))
    keyboard.add(InlineKeyboardButton("News", callback_data="news"))
    keyboard.add(InlineKeyboardButton("Contacts", callback_data="contacts"))
    keyboard.add(InlineKeyboardButton("FAQ", callback_data="faq"))
    keyboard.add(InlineKeyboardButton("Partners", callback_data="partners"))
    keyboard.add(InlineKeyboardButton("Investors", callback_data="investors"))
    await message.reply("Welcome! Choose an option:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "company_info")
async def process_company_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = get_paginated_keyboard(CompanyInfo)
    await bot.send_message(
        callback_query.from_user.id, "Company Info:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data.startswith("CompanyInfo_page_"))
async def process_company_info_page(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split("_")[-1])
    await bot.answer_callback_query(callback_query.id)
    keyboard = get_paginated_keyboard(CompanyInfo, page)
    await bot.send_message(
        callback_query.from_user.id, "Company Info:", reply_markup=keyboard
    )


# Define similar handlers for Services, News, Contacts, FAQ, Partners, Investors


@dp.callback_query_handler(lambda c: c.data == "partners")
async def process_partners(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("View Partners", callback_data="view_partners"))
    keyboard.add(
        InlineKeyboardButton("Apply for Partnership", callback_data="apply_partnership")
    )
    keyboard.add(InlineKeyboardButton("Back", callback_data="start"))
    await bot.send_message(
        callback_query.from_user.id, "Partners:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "view_partners")
async def process_view_partners(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = get_paginated_keyboard(Partner)
    await bot.send_message(
        callback_query.from_user.id, "Partners:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "apply_partnership")
async def process_apply_partnership(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Please send your full name:")
    # Implement logic to collect user input and save to ApplicationPartners


@dp.callback_query_handler(lambda c: c.data == "investors")
async def process_investors(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("View Investors", callback_data="view_investors"))
    keyboard.add(
        InlineKeyboardButton("Apply for Investment", callback_data="apply_investment")
    )
    keyboard.add(InlineKeyboardButton("Back", callback_data="start"))
    await bot.send_message(
        callback_query.from_user.id, "Investors:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "view_investors")
async def process_view_investors(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = get_paginated_keyboard(Investor)
    await bot.send_message(
        callback_query.from_user.id, "Investors:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "apply_investment")
async def process_apply_investment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Please send your full name:")
    # Implement logic to collect user input and save to ApplicationInvestors


class Command(BaseCommand):
    help = "Start the Telegram bot"

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
