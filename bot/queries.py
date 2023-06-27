create_table_dishes = """
CREATE TABLE IF NOT EXISTS dishes (
    d_id INT,
    dish_name TEXT NOT NULL,
    bot_command TEXT NOT NULL,
    category TEXT NOT NULL,
    rating INT,
    PRIMARY KEY (d_id))
"""

create_table_ingredients = """
CREATE TABLE IF NOT EXISTS ingredients (
    i_id INT,
    dish_id INT,
    name TEXT NOT NULL,
    amount FLOAT,
    FOREIGN KEY (dish_id) REFERENCES dishes(d_id))
"""

create_table_user_cart = """
CREATE TABLE IF NOT EXISTS user_cart (
	id	INTEGER NOT NULL UNIQUE,
	user_id	INT UNIQUE,
	cart	TEXT,
	PRIMARY KEY(id AUTOINCREMENT))
"""



