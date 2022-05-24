from loader import dp,db
from aiogram import types
from states.product import Shop
from aiogram.dispatcher import FSMContext
from keyboards.inline.amuont import numbers

@dp.message_handler(state=Shop.Praduct)
async def get_prod(message: types.message,state: FSMContext):
    prod_name = message.text
    data = await state.get_data()
    cat_id = data.get("cat_id")
    info = db.get_praduct_title_id(title=prod_name,cat_id=cat_id)
    await state.update_data(
        {'title': str(info[1]),'price': info[3]}
    )
    await message.answer_photo(photo=info[4],caption=f"<b>{info[1]}\n\nBatasil: {info[2]}\n\nNarxi: {info[3]} So'm\n</b>",reply_markup=numbers)
    await Shop.next()