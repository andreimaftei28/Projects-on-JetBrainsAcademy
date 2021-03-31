"""
Script for creating a simple backend system that alows creating and working
with a database, with the help of sqlite module
"""

import argparse
import sqlite3
import sys
from sqlite3 import Error

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
parser = argparse.ArgumentParser()
parser.add_argument("Database", help="Database name")
parser.add_argument("--ingredients", help="ingredients to search into recipe")
parser.add_argument("--meals", help="type of the meal where a recipe can be served")
args = parser.parse_args()


def create_connection(db_file):
    """Creates a connection to the database"""

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_sql_table):
    """Creates tables inside the database"""

    try:
        curr = conn.cursor()
        curr.execute("PRAGMA foreign_keys = ON")
        curr.execute(create_sql_table)
        conn.commit()
    except Error as e:
        print(e)


def insert(conn, table, item):
    """Inserts data into tables"""

    curr = conn.cursor()
    sql = f"INSERT INTO {table}({table[:-1]}_name) VALUES('{item}');"
    curr.execute(sql)
    conn.commit()
    return


def select_from_table(conn, table):
    """Selects all data from specific table and prints the result in a nice formated way"""

    cur = conn.cursor()
    sql = f"SELECT * FROM {table}"
    result = cur.execute(sql)
    all_data = result.fetchall()
    for dat in all_data:
        print(") ".join([str(dat[0]), dat[1]]), end="\t")
    print()


def feed_database(conn):
    """Containes the sql queries for creating the tables, retrieves data from tables and inserts
    into tables accordingly"""

    sql_ingredients_table = """CREATE TABLE IF NOT EXISTS ingredients (
                                    ingredient_id INTEGER PRIMARY KEY,
                                    ingredient_name TEXT NOT NULL UNIQUE
                                    );"""
    sql_measures_table = """CREATE TABLE IF NOT EXISTS measures (
                                        measure_id INTEGER PRIMARY KEY,
                                        measure_name TEXT UNIQUE
                                        );"""
    sql_meals_table = """CREATE TABLE IF NOT EXISTS meals (
                                        meal_id INTEGER PRIMARY KEY,
                                        meal_name TEXT NOT NULL UNIQUE
                                        );"""
    sql_recipes_table = """CREATE TABLE IF NOT EXISTS recipes (
                                            recipe_id INTEGER PRIMARY KEY,
                                            recipe_name TEXT NOT NULL,
                                            recipe_description TEXT
                                            );"""
    sql_serve_table = """CREATE TABLE IF NOT EXISTS serve (
                                                serve_id INTEGER PRIMARY KEY,
                                                recipe_id INTEGER NOT NULL,
                                                meal_id INTEGER NOT NULL,
                            FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
                            FOREIGN KEY(meal_id) REFERENCES meals(meal_id));"""
    sql_quantity_table = """CREATE TABLE IF NOT EXISTS quantity (
                                                    quantity_id INTEGER PRIMARY KEY,
                                                    quantity INTEGER NOT NULL,
                                                    recipe_id INTEGER NOT NULL,
                                                    measure_id INTEGER NOT NULL,
                                                    ingredient_id INTEGER NOT NULL,
                                FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
                                FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
                                FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id));"""

    if conn is not None:
        create_table(conn, sql_ingredients_table)
        create_table(conn, sql_measures_table)
        create_table(conn, sql_meals_table)
        create_table(conn, sql_recipes_table)
        create_table(conn, sql_serve_table)
        create_table(conn, sql_quantity_table)

    else:
        print("Error! cannot create the database connection.")
    with conn:
        for table in data:
            for item in data[table]:
                try:
                    insert(conn, table, item)
                except sqlite3.IntegrityError:
                    pass
        curr = conn.cursor()
        while True:
            recipe_name = input("Recipe name: ")
            if recipe_name == "":
                break
            else:
                recipe_description = input("Recipe description: ")
                recipe_id = curr.execute(f"INSERT INTO recipes(recipe_name, recipe_description)\
                 VALUES('{recipe_name}', '{recipe_description}')").lastrowid
                conn.commit()
                select_from_table(conn, "meals")
                served = tuple(map(int, input("Enter proposed meals separated by a space: ").split()))
                for meal in served:
                    curr.execute(f"INSERT INTO serve(meal_id, recipe_id) VALUES('{meal}', '{recipe_id}')")
                conn.commit()
                while True:
                    ingredient = input("Input quantity of ingredient <press enter to stop>: ").split()
                    if len(ingredient) == 0:
                        break
                    else:
                        try:
                            ingredient[0] = int(ingredient[0])
                        except ValueError:
                            print("Quantity should be an integer.")
                        if any([len(ingredient) < 2, len(ingredient) > 3]):
                            print("Wrong form! Should be [quantity <measure> ingredient]!")
                        else:
                            if len(ingredient) == 2:
                                measure_id = curr.execute(
                                    f"SELECT measure_id FROM measures WHERE measure_name = ''").fetchall()
                                ingredient_id = curr.execute(
                                    f"SELECT ingredient_id FROM ingredients "
                                    f"WHERE ingredient_name LIKE '%{ingredient[1]}%'").fetchall()
                            else:
                                measure_id = curr.execute(
                                    f"SELECT measure_id FROM measures "
                                    f"WHERE measure_name LIKE '{ingredient[1]}%'").fetchall()
                                ingredient_id = curr.execute(
                                    f"SELECT ingredient_id FROM ingredients "
                                    f"WHERE ingredient_name LIKE '%{ingredient[2]}%'").fetchall()

                            if len(measure_id) == 0:
                                print("There is no such measure!")
                            elif len(ingredient_id) == 0:
                                print("There is no such ingredient!")
                            elif len(measure_id) != 1:
                                print("The measure is not conclusive!")
                            elif len(ingredient_id) != 1:
                                print("The ingredient is not conclusive!")
                            else:
                                curr.execute(f"INSERT INTO quantity(quantity, recipe_id, measure_id, ingredient_id) "
                                             f"VALUES('{ingredient[0]}', '{recipe_id}', '{measure_id[0][0]}','{ingredient_id[0][0]}')")
                                conn.commit()

    conn.close()


def retrieve_data(conn, ingredients, meals):
    """If extra arguments are passed to the script this function retrieves data from tables
    according to the arguments that are passed in"""

    curr = conn.cursor()
    quantity, temp, quantity_out = [], [], []
    for ingredient in ingredients.split(","):
        quantity.append(set(number[0] for number in curr.execute(
            f"SELECT recipe_id FROM quantity WHERE ingredient_id in (SELECT ingredient_id FROM ingredients WHERE ingredient_name = '{ingredient}')").fetchall()))
    quantity = set.intersection(*quantity)
    for meal in meals.split(","):
        temp.append(set(number[0] for number in curr.execute(
            f"SELECT recipe_id FROM serve WHERE meal_id in (SELECT meal_id FROM meals WHERE meal_name = '{meal}')").fetchall()))
    if len(meals.split(",")) == 1:
        quantity_out = set.intersection(*temp)
    else:
        for item in [*temp]:
            for q in item:
                if q in quantity:
                    quantity_out.append(q)

    recipes = ", ".join(
        [curr.execute(f"SELECT recipe_name FROM recipes WHERE recipe_id = '{id_}'").fetchone()[0] for id_ in
         set.intersection(quantity, quantity_out)])

    print(f"Recipes selected for you: {recipes}" if recipes else "There are no such recipes in the database.")
    conn.close()


def main():

    if not args.ingredients:
        database = sys.argv[-1]
        conn = create_connection(database)
        feed_database(conn)
    else:
        database = args.Database
        conn = create_connection(database)
        retrieve_data(conn, args.ingredients, args.meals)


if __name__ == '__main__':
    main()
