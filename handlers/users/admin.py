import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from states.product import category,Praduct
from aiogram.dispatcher import FSMContext
from datetime import datetime


@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       

@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")


@dp.message_handler(text="/Cart", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_cart()
    await message.answer("Baza tozalandi!")

@dp.message_handler(commands=["category"],user_id=ADMINS)
async def go_staert(message: types.message):
    await message.answer("Qo'shmoqchi bo'lgan kateg'o'ryani kiriting")
    await category.title.set()



@dp.message_handler(state=category.title,user_id=ADMINS)
async def add_cat(message: types.message,state: FSMContext):
    category = message.text
    await message.answer(f"{category} bazaga qo'shildi")
    db.add_category_title(title=str(category))
    await state.finish()


@dp.message_handler(commands=["Praduct"],user_id=ADMINS)
async def add_category(message: types.message):
    await message.answer("Qo'shmoqcho bo'lgan maxsulotingiz kiriting")
    await Praduct.title.set()


@dp.message_handler(state=Praduct.title,user_id=ADMINS)
async def get_name(message: types.message,state:FSMContext):
    title = message.text
    await state.update_data(
        {"title": title}
    )
    await message.answer("Batafsil malumot kiriting")
    await Praduct.next()

@dp.message_handler(state=Praduct.description,user_id=ADMINS)
async def get_name(message: types.message,state:FSMContext):
    description = message.text
    await state.update_data(
        {"description": description}
    )
    await message.answer("Maxsulot narxini kiriting (so'm)")
    await Praduct.next()


@dp.message_handler(state=Praduct.price,user_id=ADMINS)
async def get_name(message: types.message,state:FSMContext):
    price= message.text
    await state.update_data(
        {"price":price}
    )
    await message.answer("Maxsulot rasmni kiriting ")
    await Praduct.next()


@dp.message_handler(content_types=["photo"],state=Praduct.image,user_id=ADMINS)
async def get_photo(message: types.message,state:FSMContext):
    image = message.photo[-1].file_id
    await state.update_data(
        {"image": image}
    )
    cats = db.select_all_cats()
    s = ""
    for cat in cats:
        s += f"{cat[0]}. {cat[1]}\n"
    await message.answer(f"Qatig'o'ryani tanlang\n\n{s}")
    await Praduct.next()

@dp.message_handler(state=Praduct.cat_id,user_id=ADMINS)
async def get_cats(message: types.message,state:FSMContext):
    cat_id = int(message.text)
    data = await state.get_data()
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    image = data.get("image")
    date_1 = datetime.now()
    db.add_praducts(title=title, description=description, price=price, image=image, data=date_1, cat_id=cat_id)
    await message.answer(f"{title} Maxsulot qo'shildi ")
    await state.finish()


@dp.message_handler(commands=['allpraduct'],user_id=ADMINS)
async def get_praduct_all(message: types.message):
    prods = db.select_all_prods()
    for i in prods:
        await message.answer_photo(photo=i[4],caption=f"Nomi: {i[1]}\nMa'lumot: {i[2]}\nNarx: {i[3]} So'm\nSana: {i[5]}")