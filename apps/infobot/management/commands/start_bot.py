import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.utils.exceptions import BadRequest
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from apps.infobot.models import (
    CompanyInfo,
    ApplicationPartner,
    Partner,
    Investor,
    ApplicationInvestor,
    Service,
    News,
    Contact,
    FAQ,
)
from core import settings


class PartnershipForm(StatesGroup):
    full_name = State()
    phone = State()
    address = State()
    user_message = State()


class InvestmentForm(StatesGroup):
    full_name = State()
    phone = State()
    address = State()
    user_message = State()


API_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN")

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(str(_("Company Info")), callback_data="company_info")
    )
    keyboard.add(InlineKeyboardButton(str(_("Services")), callback_data="services"))
    keyboard.add(InlineKeyboardButton(str(_("News")), callback_data="news"))
    keyboard.add(InlineKeyboardButton(str(_("Contacts")), callback_data="contacts"))
    keyboard.add(InlineKeyboardButton(str(_("FAQ")), callback_data="faq"))
    keyboard.add(InlineKeyboardButton(str(_("Partners")), callback_data="partners"))
    keyboard.add(InlineKeyboardButton(str(_("Investors")), callback_data="investors"))
    keyboard.add(InlineKeyboardButton(str(_("Inline")), callback_data="inline"))
    await message.reply(str(_("Welcome! Choose an option:")), reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "start")
async def process_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Company Info", callback_data="company_info"))
    keyboard.add(InlineKeyboardButton("Services", callback_data="services"))
    keyboard.add(InlineKeyboardButton("News", callback_data="news"))
    keyboard.add(InlineKeyboardButton("Contacts", callback_data="contacts"))
    keyboard.add(InlineKeyboardButton("FAQ", callback_data="faq"))
    keyboard.add(InlineKeyboardButton("Partners", callback_data="partners"))
    keyboard.add(InlineKeyboardButton("Investors", callback_data="investors"))
    keyboard.add(InlineKeyboardButton("Inline", callback_data="inline"))
    await bot.send_message(callback_query.from_user.id, "Welcome! Choose an option:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "inline")
async def process_inline(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "This is the Inline button action!")


@dp.callback_query_handler(lambda c: c.data == "company_info")
async def process_company_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    company_info_list = await sync_to_async(list)(CompanyInfo.objects.all())

    message_text = "Company Info:\n\n"
    for info in company_info_list:
        message_text += f"Name: {info.name}\nDescription: {info.description}\n\nPhone: {info.phone}\nEmail: {info.email}\nWebsite: {info.website}\n\n"

    await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "partners")
async def process_investors(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("View partnesr", callback_data="view_partners"))
    keyboard.add(
        InlineKeyboardButton("Apply for Partnership", callback_data="apply_partnership")
    )
    keyboard.add(InlineKeyboardButton("Back", callback_data="start"))
    await bot.send_message(
        callback_query.from_user.id, "Partnesr:", reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data == "view_partners")
async def process_view_partners(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    partner_list = await sync_to_async(list)(Partner.objects.all())

    message_text = "Partners:\n\n"
    for partner in partner_list:
        message_text += f"Name: {partner.name}\nDescription: {partner.description}\n"
        if partner.logo and partner.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(partner.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=f"Name: {partner.name}\nDescription: {partner.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += "Logo URL is invalid.\n"
        else:
            message_text += "\n"

            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "apply_partnership")
async def process_apply_partnership(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Please send your full name:")
    await PartnershipForm.full_name.set()


@dp.message_handler(state=PartnershipForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["full_name"] = message.text
    await message.reply("Please send your phone number:")
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text
    await message.reply("Please send your address:")
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await message.reply("Please send your message:")
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.user_message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_message = message.text
        await sync_to_async(ApplicationPartner.objects.create)(
            full_name=data["full_name"],
            phone=data["phone"],
            address=data["address"],
            message=user_message,
        )
    await message.reply("Your application has been submitted!")
    await state.finish()


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

    investor_list = await sync_to_async(list)(Investor.objects.all())

    message_text = "Investors:\n\n"
    for investor in investor_list:
        message_text += f"Name: {investor.name}\nDescription: {investor.description}\n"
        if investor.logo and investor.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(investor.logo)}"
            print(f"Photo Path: {photo_path}")
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=f"Name: {investor.name}\nDescription: {investor.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += "Logo URL is invalid.\n"
        else:
            message_text += "\n"
            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "apply_investment")
async def process_apply_investment(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Please send your full name:")
    await InvestmentForm.full_name.set()


@dp.message_handler(state=InvestmentForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["full_name"] = message.text
    await message.reply("Please send your phone number:")
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text
    await message.reply("Please send your address:")
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await message.reply("Please send your message:")
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.user_message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_message = message.text
        await sync_to_async(ApplicationInvestor.objects.create)(
            full_name=data["full_name"],
            phone=data["phone"],
            address=data["address"],
            message=user_message,
        )
    await message.reply("Your application has been submitted!")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "company_info")
async def process_company_info(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    company_info_list = await sync_to_async(list)(CompanyInfo.objects.all())

    message_text = "Company Info:\n\n"
    for info in company_info_list:
        message_text += f"Name: {info.name}\nDescription: {info.description}\n\nPhone: {info.phone}\nEmail: {info.email}\nWebsite: {info.website}\n\n"

    await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "services")
async def process_services(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    services_list = await sync_to_async(list)(Service.objects.all())

    message_text = "Services:\n\n"
    for service in services_list:
        message_text += f"Name: {service.name}\nDescription: {service.description}\n\n"

    await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "news")
async def process_news(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    news_list = await sync_to_async(list)(News.objects.all())

    for news in news_list:
        message_text = f"Title: {news.title}\nDescription: {news.description}\n\n"
        if news.image and news.image.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(news.image)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        callback_query.from_user.id,
                        photo,
                        caption=message_text,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await bot.send_message(callback_query.from_user.id, "Image URL is invalid.\n")
        else:
            await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "contacts")
async def process_contacts(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    contacts_list = await sync_to_async(list)(Contact.objects.all())

    message_text = "Contacts:\n\n"
    for contact in contacts_list:
        message_text += (
            f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}\n\n"
        )

    await bot.send_message(callback_query.from_user.id, message_text)


@dp.callback_query_handler(lambda c: c.data == "faq")
async def process_faq(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # Fetch FAQ data
    faq_list = await sync_to_async(list)(FAQ.objects.all())

    # Format the data into a readable message
    message_text = "FAQ:\n\n"
    for faq in faq_list:
        message_text += f"Question: {faq.question}\nAnswer: {faq.answer}\n\n"

    # Send the formatted message to the user
    await bot.send_message(callback_query.from_user.id, message_text)


class Command(BaseCommand):
    help = "Start the Telegram bot"

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
