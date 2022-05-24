from loader import dp,db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.default.cats import all_cats


@dp.callback_query_handler(text="tozalash", state=Shop.delete)
async def class_cart(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    user_id = data.get("user_id")
    print(user_id)
    db.delete_praduxts(telegram_id=user_id)
    await call.message.answer("Savat bo'shatildi")
    await call.message.answer("Asosiy saxifadasiz", reply_markup=all_cats)
    await Shop.category.set()

@dp.callback_query_handler(state=Shop.delete)
async def deleta_praduct(call: types.CallbackQuery,state:FSMContext):
    msg = "Sizning savatingiz"
    data = await state.get_data()
    user_id = data.get("user_id")
    title,telegram_id = call.data.split(":")
    db.delete_current_product(telegram_id=user_id)
    await call.answer(f"{title} Savatdan o'chirildi")
    cart = db.select_product(telegram_id=user_id)
    new = InlineKeyboardMarkup()
    for c in cart:
        msg += f" \n{c[2]} 🛒 {c[-1]} ta = {c[-1] * c[-2]}  So'm"
        new.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}: {c[1]}"))
    new.add(InlineKeyboardButton(text="Orqaga", callback_data="orqaga"))
    await  call.message.edit_reply_markup()(reply_markup=new)
    await Shop.delete.set()