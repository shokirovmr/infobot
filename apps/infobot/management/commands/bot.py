import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(str(_("Company Info"))))
    keyboard.add(KeyboardButton(str(_("Services"))))
    keyboard.add(KeyboardButton(str(_("News"))))
    keyboard.add(KeyboardButton(str(_("Contacts"))))
    keyboard.add(KeyboardButton(str(_("FAQ"))))
    keyboard.add(KeyboardButton(str(_("Partners"))))
    keyboard.add(KeyboardButton(str(_("Investors"))))
    return keyboard


def get_back_button():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(str(_("Back to Menu"))))
    return keyboard


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(str(_("Welcome! Choose an option:")), reply_markup=get_main_menu())


@dp.message_handler(lambda message: message.text == str(_("Back to Menu")))
async def back_to_menu(message: types.Message):
    await message.reply(str(_("Choose an option:")), reply_markup=get_main_menu())


@dp.message_handler(lambda message: message.text == str(_("Company Info")))
async def process_company_info(message: types.Message):
    company_info_list = await sync_to_async(list)(CompanyInfo.objects.all())

    message_text = "Company Info:\n\n"
    for info in company_info_list:
        message_text += f"Name: {info.name}\nDescription: {info.description}\n\nPhone: {info.phone}\nEmail: {info.email}\nWebsite: {info.website}\n\n"

    await message.reply(message_text, reply_markup=get_back_button())


@dp.message_handler(lambda message: message.text == str(_("Partners")))
async def process_partners(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(str(_("View Partners"))))
    keyboard.add(KeyboardButton(str(_("Apply for Partnership"))))
    keyboard.add(KeyboardButton(str(_("Back to Menu"))))
    await message.reply("Partners:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == str(_("View Partners")))
async def process_view_partners(message: types.Message):
    partner_list = await sync_to_async(list)(Partner.objects.all())

    message_text = "Partners:\n\n"
    for partner in partner_list:
        message_text += f"Name: {partner.name}\nDescription: {partner.description}\n"
        if partner.logo and partner.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(partner.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=f"Name: {partner.name}\nDescription: {partner.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += "Logo URL is invalid.\n"
        else:
            message_text += "\n"

    await message.reply(message_text, reply_markup=get_back_button())


@dp.message_handler(lambda message: message.text == str(_("Apply for Partnership")))
async def process_apply_partnership(message: types.Message):
    await message.reply("Please send your full name:", reply_markup=get_back_button())
    await PartnershipForm.full_name.set()


@dp.message_handler(state=PartnershipForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["full_name"] = message.text
    await message.reply("Please send your phone number:", reply_markup=get_back_button())
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text
    await message.reply("Please send your address:", reply_markup=get_back_button())
    await PartnershipForm.next()


@dp.message_handler(state=PartnershipForm.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await message.reply("Please send your message:", reply_markup=get_back_button())
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
    await message.reply("Your application has been submitted!", reply_markup=get_back_button())
    await state.finish()


@dp.message_handler(lambda message: message.text == str(_("Investors")))
async def process_investors(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(str(_("View Investors"))))
    keyboard.add(KeyboardButton(str(_("Apply for Investment"))))
    keyboard.add(KeyboardButton(str(_("Back to Menu"))))
    await message.reply("Investors:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == str(_("View Investors")))
async def process_view_investors(message: types.Message):
    investor_list = await sync_to_async(list)(Investor.objects.all())

    message_text = "Investors:\n\n"
    for investor in investor_list:
        message_text += f"Name: {investor.name}\nDescription: {investor.description}\n"
        if investor.logo and investor.logo.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(investor.logo)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=f"Name: {investor.name}\nDescription: {investor.description}",
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    message_text += "Logo URL is invalid.\n"
        else:
            message_text += "\n"

    await message.reply(message_text, reply_markup=get_back_button())


@dp.message_handler(lambda message: message.text == str(_("Apply for Investment")))
async def process_apply_investment(message: types.Message):
    await message.reply("Please send your full name:", reply_markup=get_back_button())
    await InvestmentForm.full_name.set()


@dp.message_handler(state=InvestmentForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["full_name"] = message.text
    await message.reply("Please send your phone number:", reply_markup=get_back_button())
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = message.text
    await message.reply("Please send your address:", reply_markup=get_back_button())
    await InvestmentForm.next()


@dp.message_handler(state=InvestmentForm.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await message.reply("Please send your message:", reply_markup=get_back_button())
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
    await message.reply("Your application has been submitted!", reply_markup=get_back_button())
    await state.finish()


@dp.message_handler(lambda message: message.text == str(_("Services")))
async def process_services(message: types.Message):
    services_list = await sync_to_async(list)(Service.objects.all())

    message_text = "Services:\n\n"
    for service in services_list:
        message_text += f"Name: {service.name}\nDescription: {service.description}\n\n"

    await message.reply(message_text, reply_markup=get_back_button())


@dp.message_handler(lambda message: message.text == str(_("News")))
async def process_news(message: types.Message):
    news_list = await sync_to_async(list)(News.objects.all())

    for news in news_list:
        message_text = f"Title: {news.title}\nDescription: {news.description}\n\n"
        if news.image and news.image.url:
            photo_path = f"{settings.MEDIA_ROOT}/{str(news.image)}"
            try:
                with open(photo_path, "rb") as photo:
                    await bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=message_text,
                    )
            except BadRequest as e:
                if "url host is empty" in str(e):
                    await message.reply("Image URL is invalid.\n", reply_markup=get_back_button())
        else:
            await message.reply(message_text, reply_markup=get_back_button())


@dp.message_handler(lambda message: message.text == str(_("Contacts")))
async def process_contacts(message: types.Message):
    contacts_list = await sync_to_async(list)(Contact.objects.all())

    message_text = "Contacts:\n\n"
    for contact in contacts_list:
        message_text += (
            f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}\n\n"
        )

    await message.reply(message_text, reply_markup=get_back_button())


@dp.message_handler(lambda message: message.text == str(_("FAQ")))
async def process_faq(message: types.Message):
    faq_list = await sync_to_async(list)(FAQ.objects.all())

    message_text = "FAQ:\n\n"
    for faq in faq_list:
        message_text += f"Question: {faq.question}\nAnswer: {faq.answer}\n\n"

    await message.reply(message_text, reply_markup=get_back_button())


class Command(BaseCommand):
    help = "Start the Telegram bot"

    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
