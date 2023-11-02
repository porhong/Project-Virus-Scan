from url_scan_API import result_control
from aiogram import Dispatcher, Bot, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
import validators
from result_to_DB import insert_result_db, select_result_db
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
    await message.answer_sticker("CAACAgIAAxkBAAEnVetlQw-BH9pz16rlSd8lAUDjolzDgQACbwAD29t-AAGZW1Coe5OAdDME")
    await message.answer("សួស្ដី🙏​ ស្វាគមន៍មកកាន់ ឆែកមើល-CheckMerl", reply_markup=link_keyboards)

# link handler


@dp.message_handler(content_types='text')
async def check_link(message: types.Message):
    await message.answer_sticker("CAACAgEAAxkBAAEnVhFlQxw2YW3MHp0eHqzCW144vfyw_wACxQIAAkeAGUTTk7G7rIZ7GjME")
    link = message.text
    validation = validators.url(link)
    if validation:

        # Select Result from DB
        result_From_DB = []
        result_From_DB = select_result_db(link)
        try:
            result_DB = result_From_DB[0]
        except:
            result_DB = ()
        # link button
        link_buttons = [
            InlineKeyboardButton(
                text='បើកតំណភ្ជាប់', url=link)]
        link_keyboards = InlineKeyboardMarkup(row_width=1)
        link_keyboards.add(*link_buttons)
        # Url Scan
        if result_From_DB != []:
            harmless = result_DB[1]
            malicious = result_DB[2]
            suspicious = result_DB[3]
            treat = result_DB[7]
            treat_count_danger = result_DB[8]
            undetected = result_DB[4]
            timeout = result_DB[5]
            result_status = result_DB[6]
            treat_count = len(treat)
            treat_name = treat

        else:
            result_list = result_control(link)
            harmless = result_list["Short_result"]["harmless"]
            malicious = result_list["Short_result"]["malicious"]
            suspicious = result_list["Short_result"]["suspicious"]
            treat = result_list["treat_status"]
            treat_count_danger = result_list["treat_count"]
            undetected = result_list["Short_result"]["undetected"]
            timeout = result_list["Short_result"]["timeout"]
            result_status = result_list["result_status"]
            treat_count = len(treat)
            try:
                treat_name = treat[0]
            except:
                treat_name = ""

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
        try:
            dd = (treat_count_danger / total_scan) * 100
        except ZeroDivisionError:
            dd = 0

        if treat_count > 0:
            result = "Danger"
        elif w > 10:
            result = "Warning"
        elif d > 10:
            result = "Danger"
        else:
            result = "Clean"

        # Status rate
        if s < 20:
            safe_status = "🟢⚪️⚪️⚪️⚪️"
        elif s < 40:
            safe_status = "🟢🟢⚪️⚪️⚪️"
        elif s < 60:
            safe_status = "🟢🟢🟢⚪️⚪️"
        elif s < 80:
            safe_status = "🟢🟢🟢🟢⚪️"
        else:
            safe_status = "🟢🟢🟢🟢🟢"

        if w < 10:
            warn_status = "⚪️⚪️⚪️⚪️⚪️"
        elif w < 20:
            warn_status = "🟠⚪️⚪️⚪️⚪️"
        elif w < 40:
            warn_status = "🟠🟠⚪️⚪️⚪️"
        elif w < 60:
            warn_status = "🟠🟠🟠⚪️⚪️"
        elif w < 80:
            warn_status = "🟠🟠🟠🟠⚪️"
        else:
            warn_status = "🟠🟠🟠🟠🟠"

        if dd < 20:
            danger_status = "🔴⚪️⚪️⚪️⚪️"
        elif dd < 40:
            danger_status = "🔴🔴⚪️⚪️⚪️"
        elif dd < 60:
            danger_status = "🔴🔴🔴⚪️⚪️"
        elif dd < 80:
            danger_status = "🔴🔴🔴🔴⚪️"
        else:
            danger_status = "🔴🔴🔴🔴🔴"

        match result:
            case"Clean":
                response_title = "<b>តំណភ្ជាប់មានសុវត្ថិភាព 🟩 </b>"
                response_note = "អ្នកអាចប្រើប្រាស់តំណភ្ជាប់នេះដោយសុវត្តិភាព។"
                response_body = f"""
 - កំរិតសុវត្ថិភាព :  {safe_status}

 - កំរិតភាពសង្ស័យ​ : {warn_status}
"""

            case"Warning":
                response_title = "<b>តំណភ្ជាប់គួរអោយសង្ស័យ 🟨 </b>"
                response_note = "សូមធ្វើការប្រើប្រាស់តំណភ្ជាប់នេះដោយមានការប្រុងប្រយ័ត្ន។"
                response_body = f"""
 - កំរិតសុវត្ថិភាព :  {safe_status}

 - កំរិតភាពសង្ស័យ​ : {warn_status}
"""
            case"Danger":
                response_title = "<b>តំណភ្ជាប់មានគ្រោះថ្នាក់ 🟥 </b>"
                response_note = "អ្នកមិនគួរបើកតំណភ្ជាប់នេះទេ ដោយតំណភ្ជាប់នេះអាចនឹងមានផ្ទុកនូវមេរោគ ឫការក្លែងបន្លំផ្សេងៗដែលអាចបង្កគ្រោះថ្នាក់។"
                response_body = f"""
 តំណភ្ចាប់នេះត្រូវបានរកឃើញការគំរាមកំហែងប្រភេទ : <strong>{treat_name.upper()}</strong>

 - កំរិតភាពគ្រោះថ្នាក់ : {danger_status}
"""
        response_message = f"""{response_title}

<b>ពត៌មានសង្ចេប</b>
{response_body}
<b>ការសន្និដ្ឋាន</b>

{response_note}

"""

        response_message_error = f"""{response_title}

<b>ពត៌មានសង្ចេប</b>
{response_body}
<b>ការសន្និដ្ឋាន</b>

{response_note}

"""
        if result == "Clean":
            await message.answer(response_message, parse_mode="html", reply_markup=link_keyboards)
            # await message.answer_sticker("CAACAgIAAxkBAAEnSyhlQiDZxwKnbTLSy8iPIBX-GO-igAACPwAD29t-AAH05pw4AeSqaTME")
        elif result == "Warning":
            await message.answer(response_message, parse_mode="html", reply_markup=link_keyboards)
            # await message.answer_sticker("CAACAgIAAxkBAAEnSyRlQiCzBcL_AfdhB4kkk_AxX0LjngACbQAD29t-AAF1HuyF8vtEpTME")
        else:
            await message.answer(response_message_error, parse_mode="html")
            # await message.answer_sticker("CAACAgIAAxkBAAEnSyBlQiAukwvBftbkAifBWLsogqYXIwACcAAD29t-AAHqAAG3tyaYON0zBA")

        # insert result to DB
        if result_From_DB == []:
            insert_result_db(link, harmless, malicious, suspicious, undetected,
                             timeout, result_status, treat_name, treat_count_danger)
    else:
        await message.answer_sticker("CAACAgIAAxkBAAEnSx5lQiAJQT6t3EVFlwzUSlLgFU-IFAACYwAD29t-AAGMnQU950KD5zME")
        await message.answer(f"""<b>តំណភ្ជាប់មិនត្រឺមត្រូវ ⚠ </b>
                            
<pre>{link}</pre>

សូមធ្វើការពិនិត្រទៅលើតំណភ្ជាប់ខាងលើ រួចព្យាយាមម្ដងទៀត។""", parse_mode="html")


async def main() -> None:
    """"Entry Point"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    executor.start_polling(dp)
