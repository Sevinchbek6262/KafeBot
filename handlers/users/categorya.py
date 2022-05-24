from loader import dp,db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

@dp.message_handler(state=Shop.category)
async def get_cat(message: types.message,state: FSMContext):
    cat_id = db.product_by_cat_id(title=message.text)
    await state.update_data(
        {"cat_id": cat_id, "categorya": message.text}
    )
    praducts = db.get_praduct_cat_id(cat_id= cat_id)
    prod = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for p in praducts:
        prod.insert(KeyboardButton(text=str(p[0:])))
    prod.add(KeyboardButton(text="Orqaga"))
    await message.answer(f"{message.text} katego'ryasidagi maxsulotlar", reply_markup=prod)
    await Shop.next()


