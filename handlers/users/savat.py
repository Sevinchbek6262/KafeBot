from loader import dp,db
from aiogram import types
from states.product import Shop
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext



@dp.message_handler(state=Shop.category,text="Savatcha🛒")
async def grt_product(message: types.message):
    cart = db.select_product(telegram_id=message.from_user.id)
    new = InlineKeyboardMarkup(row_width=2)
    if len(cart) !=0:
        msg = "Sizning savatindiz"
        for c in cart:
            msg += f" \n{c[2]} 🛒 {c[-1]} ta = {c[-1] * c[-2]}  So'm"
            new.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}: {c[1]}"))
        new.insert(InlineKeyboardButton(text="Tozalash", callback_data="tozalash"))
        new.insert(InlineKeyboardButton(text="Buyirtma berish", callback_data="buyurtma berish"))

    else:
        msg = "Sizning savatingiz bo'sh"
        new.add(InlineKeyboardButton(text="Orqaga", callback_data="orqaga"))
    await message.answer(msg, reply_markup=new)
    await Shop.delete.set()


@dp.callback_query_handler(text="savatchaa", state=Shop.amount)
async def get_savat(call: types.CallbackQuery,state: FSMContext):
    msg = "Sizning savatindiz"
    data = await state.get_data()
    user_id = data.get("user_id")
    cart = db.select_product(telegram_id=user_id)
    new = InlineKeyboardMarkup(row_width=2)
    for c in cart:
        msg += f" \n{c[2]} 🛒 {c[-1]} ta = {c[-1] * c[-2]}  So'm"
        new.insert(InlineKeyboardButton(text=f"❌ {c[2]} ❌", callback_data=f"{c[2]}: {c[1]}"))
        new.insert(InlineKeyboardButton(text="Tozalash", callback_data="tozalash"))
        new.insert(InlineKeyboardButton(text="Buyirtma berish", callback_data="buyurtma berish"))
            
    await call.message.answer(msg, reply_markup=new)
    await Shop.delete.set()
