from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

numbers = InlineKeyboardMarkup()
for i in range(1, 10):
    numbers.insert(InlineKeyboardButton(text=f"+{i}", callback_data=str(i)))
numbers.insert(InlineKeyboardButton(text="Savatcha",callback_data="savatchaa"))
numbers.insert(InlineKeyboardButton(text="Orqaga",callback_data="orqaga"))
numbers.insert(InlineKeyboardButton(text="Bosh menu",callback_data="bosh menu"))
