import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)


    def create_product_table(self):
        slq = """
        CREATE TABLE Praduct(
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            image TEXT NOT NULL,
            data DATETIME NOT NULL,
            cat_id INTEGER NOT NULL

        );
"""
        self.execute(slq,commit=True)

    def create_category_table(self):
        slqq = """
        CREATE TABLE category(
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL
            );
"""
            
        self.execute(slqq,commit=True)


    def create_cart_table(self):
        slqq = """
        CREATE TABLE Cart(
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            price INTEGER NOT NULL,
            amount INTEGER NOT NULL

            );
"""
            
        self.execute(slqq,commit=True)





    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())


    def add_category_title(self,title: str):
        sql = """
        INSERT INTO category(title) VALUES(?)
        """
        self.execute(sql,parameters=(title, ),commit=True)



    def add_praduct_cart(self,telegram_id: int, title: str, price: int, amount: int):
        sql = "SELECT * FROM Cart WHERE telegram_id=? AND title=?"
        data = self.execute(sql, parameters=(telegram_id, title), fetchone=True)
        if data:
            sql = "UPDATE Cart SET amount=? where id=? "
            self.execute(sql,parameters=(int(data[4]) + int(amount), int(data[0])),commit=True)

        else:
            sql = """
            INSERT INTO Cart(telegram_id, title, price, amount) VALUES(?, ?, ?, ?);
            """
            self.execute(sql, parameters=(telegram_id, title, price, amount), commit=True)



    def add_praducts(self,title,description, price, image, data, cat_id):
        sql = """
        INSERT INTO Praduct(title, description, price, image, data, cat_id) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql,parameters=(title, description, price, image, data, cat_id),commit=True)



    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_cats(self):
        sql = """
        SELECT * FROM category
        """
        return self.execute(sql, fetchall=True)


    def delete_current_product(self, **kwargs):
        sql = "DELETE FROM Cart where "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql,parameters=parameters, commit=True)


    def select_all_prods(self):
        sql = """
        SELECT * FROM Praduct
        """
        return self.execute(sql, fetchall=True)

    def product_by_cat_id(self, **kwargs):
        sql = "SELECT id FROM category WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        Cat_id = self.execute(sql,parameters=parameters, fetchone=True)
        return Cat_id[0]


    def get_praduct_cat_id(self, **kwargs):
        sql = "SELECT title FROM Praduct WHERE  "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql,parameters=parameters, fetchone=True)

    def get_praduct_title_id(self, **kwargs):
        sql = "SELECT * FROM Praduct WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)



    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_product(self, **kwargs):
        sql = "SELECT * FROM Cart WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)





    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE ", commit=True)

    def delete_cart(self):
        self.execute("DELETE FROM Cart WHERE TRUE ", commit=True)


    def delete_praduxts(self,telegram_id):
        sql = "DELETE FROM Cart WHERE telegram_id=?"
        self.execute(sql, (telegram_id, ), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
