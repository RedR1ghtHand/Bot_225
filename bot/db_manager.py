import sqlite3
import queries

class DB_Manager():
    _db = 'menu_data.db'

    @staticmethod
    def create_db(query, db = _db):
        try:
            sql_con = sqlite3.connect(db)
            cursor = sql_con.cursor()
            print('Connected')
            cursor.execute(query)
            sql_con.commit()
            print('table created')
            cursor.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            sql_con.close()
            print("connection is closed")


    @staticmethod
    def get_ingredients_by_dish_comand(dish, db = _db):
        try:
            sqlite_con = sqlite3.connect(db, timeout=20)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")
            cursor.execute("""SELECT name, amount
                              FROM ingredients i
                              JOIN dishes d ON d.d_id = i.dish_id
                              WHERE d.dish_name = '{dish}'""".format(dish=dish))
            result = cursor.fetchall()
            cursor.close()
            return result

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    @staticmethod
    def get_ingredients_by_dish_name(dish, db=_db):
        try:
            sqlite_con = sqlite3.connect(db, timeout=20)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")
            cursor.execute("""SELECT name, amount
                                  FROM ingredients i
                                  JOIN dishes d ON d.d_id = i.dish_id
                                  WHERE d.bot_command = '{dish}'""".format(dish=dish))
            result = cursor.fetchall()
            cursor.close()
            return result

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    # @staticmethod
    # def get_list_from_ingredients(db = _db):
    #     try:
    #         sqlite_con = sqlite3.connect(db, timeout=20)
    #         cursor = sqlite_con.cursor()
    #         sqlite_select_list_from_ingredients = """SELECT name from ingredients"""
    #
    #         cursor.execute(sqlite_select_list_from_ingredients)
    #
    #         result = [item[0] for item in cursor.fetchall()]
    #         cursor.close()
    #         return set(result)
    #
    #     except sqlite3.Error as error:
    #         print("Failed to read data from sqlite table", error)
    #
    #     finally:
    #         sqlite_con.close()
    #         print("The Sqlite connection is closed")

    @staticmethod
    def get_list_from_dishes(db = _db):
        try:
            sqlite_con = sqlite3.connect(db, timeout=20)
            cursor = sqlite_con.cursor()
            sqlite_select_query_dish = """SELECT dish_name, bot_command 
                                          FROM dishes"""
            cursor.execute(sqlite_select_query_dish)
            dish_list = cursor.fetchall()
            cursor.close()
            return dish_list

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    @staticmethod
    def add_rating(dish: str, point=1, db = _db):
        try:
            sqlite_con = sqlite3.connect(db, timeout=20)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")

            sqlite_update_rating = """UPDATE dishes SET rating = rating + {point}
                                      WHERE bot_command = '{dish}' """.format(dish=dish, point=point)

            cursor.execute(sqlite_update_rating)
            sqlite_con.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    @staticmethod
    def get_dish_rating(db = _db) -> list:
        try:
            sqlite_con = sqlite3.connect(db, timeout=20)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")

            get_dish_rating_query = """SELECT bot_command, rating from dishes
                                     ORDER BY rating DESC"""

            cursor.execute(get_dish_rating_query)
            dish_by_rating = cursor.fetchmany(3)
            cursor.close()
            return dish_by_rating

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    @staticmethod
    def create_user_cart(user_id, db = _db):
        try:
            sqlite_con = sqlite3.connect(db)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")

            sqlite_create_cart = f"""INSERT INTO user_cart (user_id, cart)
                                    VALUES ({user_id}, '')"""

            cursor.execute(sqlite_create_cart)
            print(f'User(cart_id:"{user_id}") cart CREATED')
            sqlite_con.commit()

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    @staticmethod
    def get_user_cart(user_id, db = _db):
        try:
            sqlite_con = sqlite3.connect(db, timeout=20)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")

            sqlite_show_user_cart = f"""SELECT cart FROM user_cart
                                        WHERE user_id = {user_id}"""

            cursor.execute(sqlite_show_user_cart)
            data = cursor.fetchone()
            sqlite_con.commit()
            cursor.close()
            return data

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    @staticmethod
    def get_user_cart_str(user_id, db = _db):
        try:
            sqlite_con = sqlite3.connect(db, timeout=20)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")

            sqlite_show_user_cart = f"""SELECT cart FROM user_cart
                                        WHERE user_id = {user_id}"""


            cursor.execute(sqlite_show_user_cart)
            data = cursor.fetchone()
            user_cart = DB_Manager.get_user_cart(user_id)[0].split('/')
            user_cart_dict = {item: user_cart.count(item) for item in user_cart if item != ''}
            user_cart_str = ''
            for item, count in user_cart_dict.items():
                user_cart_str += f'{item} : {str(count)}\n'

            sqlite_con.commit()
            cursor.close()
            return user_cart_str

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")

    @staticmethod
    def add_to_cart(user_id: int, data: str, db = _db):
        try:
            sqlite_con = sqlite3.connect(db)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")

            sqlite_update_cart = f"""UPDATE user_cart
                                     SET cart = cart || '/{data}'
                                     WHERE user_id = {user_id}"""

            cursor.execute(sqlite_update_cart)
            sqlite_con.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")


    @staticmethod
    def clear_user_cart(user_id: int, db = _db):
        try:
            sqlite_con = sqlite3.connect(db)
            cursor = sqlite_con.cursor()
            print("Connected to SQLite")

            sqlite_clear_cart = f"""UPDATE user_cart
                                    SET cart = ''
                                    WHERE user_id = {user_id}"""

            cursor.execute(sqlite_clear_cart)
            sqlite_con.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)

        finally:
            sqlite_con.close()
            print("The Sqlite connection is closed")






if __name__ == '__main__':
    db = DB_Manager()
    print(db.get_ingredients_by_dish_name('Роли'))
    # db.create_db(queries.create_table_user_cart)
    # db.create_user_cart('222')

    # res = db.get_ingredients_by_dish('o_nigiri')
    #
    # print(db.get_user_cart('111'))
    #
    # for i in res:
    #     print(i[0], ':', i[1])