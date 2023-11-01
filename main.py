import requests
import json
from url_scan_API import result_control
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
    await message.answer_sticker("CAACAgIAAxkBAAEnSpZlQhedfApj13TDMdyBPy0Iw5it3gACXwAD29t-AAGEsFSbEa7K4zME")
    message_id = message.message_id
    link = message.text
    validation = validators.url(link)
    if validation:
        # Url Scan
        result_list = result_control(link)
        harmless = result_list["Short_result"]["harmless"]
        malicious = result_list["Short_result"]["malicious"]
        suspicious = result_list["Short_result"]["suspicious"]
        treat = result_list["treat_status"]
        treat_count = len(treat)
        print(treat)
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

        if treat_count > 0:
            result = "Danger"
        elif w > 10:
            result = "Warning"
        elif d > 10:
            result = "Danger"
        else:
            result = "Clean"
        match result:
            case"Clean":
                response_title = "<b>តំណភ្ជាប់មានសុវត្ថិភាព 🟩 </b>"
                response_note = "អ្នកអាចប្រើប្រាស់តំណភ្ជាប់នេះដោយសុវត្តិភាព។"
                response_body = f"""
 - មានសុវត្ថិភាព : {s:.1f}%
 - មានភាពសង្ស័យ​ : {w:.1f}%
"""

            case"Warning":
                response_title = "<b>តំណភ្ជាប់គួរអោយសង្ស័យ 🟨 </b>"
                response_note = "សូមធ្វើការប្រើប្រាស់តំណភ្ជាប់នេះដោយមានការប្រុងប្រយ័ត្ន។"
                response_body = f"""
 - មានសុវត្ថិភាព : {s:.1f}%
 - មានភាពសង្ស័យ​ : {w:.1f}%
"""
            case"Danger":
                response_title = "<b>តំណភ្ជាប់មានគ្រោះថ្នាក់ 🟥 </b>"
                response_note = "អ្នកមិនគួរបើកតំណភ្ជាប់នេះទេ ដោយតំណភ្ជាប់នេះអាចនឹងមានផ្ទុកនូវមេរោគ ឫការក្លែងបន្លំផ្សេងៗដែលអាចបង្កគ្រោះថ្នាក់។"
                response_body = f"""
 តំណភ្ចាប់នេះត្រូវបានរកឃើញការគំរាមកំហែងប្រភេទ : <strong>{treat[0].upper()}</strong>
"""
        response_message = f"""{response_title}

<b>ពត៌មានសង្ចេប</b>
{response_body}
<b>ការសន្និដ្ឋាន</b>

{response_note}

<b>តំណភ្ជាប់</b>
        

{link}"""

        response_message_error = f"""{response_title}

<b>ពត៌មានសង្ចេប</b>
{response_body}
<b>ការសន្និដ្ឋាន</b>

{response_note}

"""
        if result == "Clean":
            await message.answer(response_message, parse_mode="html")
            await message.answer_sticker("CAACAgIAAxkBAAEnSyhlQiDZxwKnbTLSy8iPIBX-GO-igAACPwAD29t-AAH05pw4AeSqaTME")
        elif result == "Warning":
            await message.answer(response_message, parse_mode="html")
            await message.answer_sticker("CAACAgIAAxkBAAEnSyRlQiCzBcL_AfdhB4kkk_AxX0LjngACbQAD29t-AAF1HuyF8vtEpTME")
        else:
            await message.answer(response_message_error, parse_mode="html")
            await message.answer_sticker("CAACAgIAAxkBAAEnSyBlQiAukwvBftbkAifBWLsogqYXIwACcAAD29t-AAHqAAG3tyaYON0zBA")

    else:
        await message.answer(f"""<b>តំណភ្ជាប់មិនត្រឺមត្រូវ ⚠ </b>
                             
<pre>{link}</pre>

សូមធ្វើការពិនិត្រទៅលើតំណភ្ជាប់ខាងលើ រួចព្យាយាមម្ដងទៀត។""", parse_mode="html")
        await message.answer_sticker("CAACAgIAAxkBAAEnSx5lQiAJQT6t3EVFlwzUSlLgFU-IFAACYwAD29t-AAGMnQU950KD5zME")


async def main() -> None:
    """"Entry Point"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    executor.start_polling(dp)
