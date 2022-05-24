from loader import dp,db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from keyboards.default.cats import all_cats



# @dp.callback_query_handler(state=Shop.delete)
# async def deleta_praduct(call: types.CallbackQuery,state:FSMContext):
#     msg = "Sizning savatindiz"
#     data = await state.get_data()
#     user_id = data.get("user_id")
#     title,telegram_id = call.data.split(":")
#     db.delete_current_product(telegram_id=user_id)
#     await call.answer(f"{title} Savatdan o'chirildi")
#     cart = db.select_product(telegram_id=user_id)
#     new = InlineKeyboardMarkup()
#     for c in cart:
#         msg += f" \n{c[2]} 🛒 {c[-1]} ta = {c[-1] * c[-2]}  So'm"
#         new.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}: {c[1]}"))
#     new.add(InlineKeyboardButton(text="Orqaga", callback_data="orqaga"))
#     await  call.message.edit_text(msg, reply_markup=new)
#     await Shop.delete.set()

@dp.callback_query_handler(state=Shop.amount)
async def get_amuant(call: types.CallbackQuery,state: FSMContext):
    amuont = call.data
    data = await state.get_data()
    title = data.get("title")
    price = data.get("price")
    user_id = data.get("user_id")
    await call.answer(f" {amuont} ta {title} Savatga qo'shildi",show_alert=True)
    await call.message.answer("Asosiy saxifa", reply_markup=all_cats)
    db.add_praduct_cart(telegram_id=user_id, title=title, price=price, amount=amuont)
    await call.message.delete()
    await Shop.category.set()
