import requests
import json
import url_scan_API
from aiogram import Dispatcher, Bot, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
import validators

# bot
bot = Bot(token="6867931343:AAEA2Tgm94emgHjGpxNujkYpgQBAWUlwi08")
dp = Dispatcher(bot)
link = ""


@dp.message_handler(commands='start')
async def hello(message: types.Message):
    # Start handler
    start_button = ['Start']
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboards.add(*start_button)

    # Inline Button
    link_buttons = [
        InlineKeyboardButton(
            text='Badbot Solution', url='https://badbotsolution.xyz')
    ]
    link_keyboards = InlineKeyboardMarkup(row_width=1)
    link_keyboards.add(*link_buttons)

    await message.answer("សួស្ដី🙏​ ស្វាគមន៍មកកាន់ ឆែកមើល-CheckMerl", reply_markup=link_keyboards)

# link handler


@dp.message_handler(content_types='text')
async def check_link(message: types.Message):
    link = message.text
    validation = validators.url(link)
    if validation:
        # Url Scan
        result_list = url_scan_API.get_link_result(
            url_scan_API.post_link(link))
        harmless = result_list["Short_result"]["harmless"]
        malicious = result_list["Short_result"]["malicious"]
        suspicious = result_list["Short_result"]["suspicious"]
        total_scan = harmless + malicious + suspicious
        try:
            s = (harmless / total_scan) * 100
        except ZeroDivisionError:
            s = 0
        try:
            w = (malicious / total_scan) * 100
        except ZeroDivisionError:
            w = 0
        try:
            d = (suspicious / total_scan) * 100
        except ZeroDivisionError:
            d = 0

        if w > 30:
            result = "Warning"
        elif d > 10:
            result = "Danger"
        else:
            result = "Clean"
        match result:
            case"Clean":
                response_title = "<b>តំណភ្ជាប់មានសុវត្ថិភាព 🟩 </b>"
                response_note = "អ្នកអាចប្រើប្រាស់តំណភ្ជាប់នេះដោយសុវត្តិភាព។"
            case"Warning":
                response_title = "<b>តំណភ្ជាប់គួរអោយសង្ស័យ 🟨 </b>"
                response_note = "សូមធ្វើការប្រើប្រាស់តំណភ្ជាប់នេះដោយមានការប្រុងប្រយ័ត្ន។"
            case"Danger":
                response_title = "<b>តំណភ្ជាប់មានគ្រោះថ្នាក់ 🟥 </b>"
                response_note = "អ្នកមិនគួរបើកតំណភ្ជាប់នេះទេ ដោយតំណភ្ជាប់នេះអាចនឹងមានផ្ទុកនូវមេរោគ ឫការក្លែងបន្លំផ្សេងៗ។"
        response_message = f"""{response_title}

<b>ពត៌មានសង្ចេប</b>

    - មានសុវត្ថិភាព : {s:.1f}%
    - គួរឱ្យសង្ស័យ​ : {w:.1f}%
    - មានគ្រោះថ្នាក់ : {d:.1f}%

<b>ការសន្និដ្ឋាន</b>

    {response_note}

<b>តំណភ្ជាប់</b>

    {link}"""
        await message.answer(response_message, parse_mode="html")
    else:
        await message.answer(f"""<b>តំណភ្ជាប់មិនត្រឺមត្រូវ ⚠ </b>
                             
<pre>{link}</pre>

សូមធ្វើការពិនិត្រទៅលើតំណភ្ជាប់ខាងលើ រួចព្យាយាមម្ដងទៀត។""", parse_mode="html")


async def main() -> None:
    """"Entry Point"""
    await dp.start_polling(bot)

if __name__ == "__main__":
  executor.start_polling(dp)
