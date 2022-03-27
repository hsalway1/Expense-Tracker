import sqlite3
import datetime

connection = sqlite3.connect("Expense tracker.db")  # connecting with the database
database = connection.cursor()

# database.execute("DROP TABLE expense_tracker")
# creating table in the database
'''
database.execute("""CREATE TABLE expense_tracker (Expenses REAL,
                          CURRENCY TEXT,
                          CATEGORY TEXT,
                          MESSAGE TEXT,
                          TIME TEXT,
                         DATE TEXT)""")'''


# database.execute("DROP TABLE Categories")

# database.execute("CREATE TABLE budget( BUDGET REAL)")
# database.execute("CREATE TABLE Categories(CATEGORIES TEXT)")


# print(database.fetchone()[0])
connection.commit()
connection.close()

