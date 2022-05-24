from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from loader import db


categorys = db.select_all_cats()

all_cats = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
for cat in categorys:
    cat_id = db.product_by_cat_id(title=cat[1])
    praducts = db.get_praduct_cat_id(cat_id= cat_id)
    # if len(praducts) != 0:
    all_cats.insert(KeyboardButton(text=cat[1]))
all_cats.row("Savatcha🛒")