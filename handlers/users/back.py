from loader import dp,db
from aiogram import types
from states.product import Shop
from keyboards.default.cats import all_cats
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

@dp.message_handler(text= "Orqaga", state= Shop.Praduct)
async def hone(message: types.message):
    await message.answer("Asosiy sahifadasiz", reply_markup=all_cats)
    await Shop.category.set()


@dp.message_handler(text="orqaga",state=Shop.amount)
async def get_praductss(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    cat_id = data.get("cat_id")
    categoriya = data.get("categorya")
    praducts = db.get_praduct_cat_id(cat_id= cat_id)
    prod = ReplyKeyboardMarkup()
    for p in praducts:
        prod.insert(KeyboardButton(text=str(p[0:])))
    prod.add(KeyboardButton(text="Orqaga"))
    await call.message.answer(f"{categoriya} katego'ryasidagi maxsulotlar", reply_markup=prod)
    await Shop.Praduct.set()

@dp.callback_query_handler(text= "orqaga", state=Shop.delete)
async def get_mayin(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.ansver("Qateg'orya tanlang",reply_markup=all_cats)
    await shop.category.set()




@dp.callback_query_handler(text= "bosh menu",state=Shop.amount)
async def get_start(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Asosiy sahifadasiz kerakli kadego'ryani tanlanf",reply_markup=all_cats)
    await Shop.category.set()