from aiogram.dispatcher.filters.state import StatesGroup,State

class category(StatesGroup):
    title = State()
    

class Praduct(StatesGroup):
    title = State()
    description = State()
    price = State()
    image = State()
    cat_id = State()



class Shop(StatesGroup):
    category = State()
    Praduct = State()
    amount = State()
    delete =State()
