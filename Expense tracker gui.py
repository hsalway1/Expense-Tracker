from tkinter import *  # for gui
import tkinter.font as font  # for changing font
import datetime  # for giving the current date and time
import sqlite3  # for connecting and making changes to the database
import tkinter.messagebox  # for appearing message box when required
from tkinter import ttk  # for create tree view table for displaying expenses
import matplotlib.pyplot as plt
from tkcalendar import *

connection = sqlite3.connect("Expense tracker.db")  # connecting to the database
database = connection.cursor()
# ---------------------------------------------***main***--------------------------------------------------------------#
window = Tk(className='Expense Tracker')  # the main frame1
window.title("Expense Tracker")
window.geometry("1200x700")  # size of the frame1
status = IntVar()  # for the status of the category check button in the second frame
# ----------------------------------------------------------Photos-----------------------------------------------------#
photo = PhotoImage(file=r"add expense.png")
photo1 = PhotoImage(file=r"icon.png")
photo3 = PhotoImage(file=r"delete1.png")
photo3 = photo3.subsample(15, 15)
settings_photo = PhotoImage(file=r"settings.png")
report_photo = PhotoImage(file=r"report.png")
graph_photo = PhotoImage(file=r"graph.png")
exit_photo = PhotoImage(file=r"exit.png")
add_photo = PhotoImage(file=r"add.png")
# -------------------------------------------------start frame---------------------------------------------------------#
start_frame = Frame(window)
main_label = Label(start_frame, text='EXPENSE TRACKER', fg='green', image=photo1, font=font.Font(size=60), compound=TOP)
main_label.place(x=350, y=100)
quote = Label(start_frame, font=font.Font(size=20), fg='brown')
quote.place(x=400, y=400)
start_frame.pack(expand=TRUE, fill='both')
# --------------------------------------------------------frames-------------------------------------------------------#
frame1 = Frame(window)
frame2 = Frame(window)
frame3 = Frame(window)
my_font = font.Font(family='Times New Roman', size=40, underline=1)  # title font
font2 = font.Font(size=20)  # font size
font3 = font.Font(size=30)
# ---------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------defaults---------------------------------------------------#
category = 'General'  # default category

currency = '₹ INR'  # default currency

category2 = ''  # default category for frame2

category3 = ''  # default category for frame3

sort = False  # for sort function


# -------------------------------------------------MAIN PROGRAM--------------------------------------------------------#


def refresh_func():  # for the refresh button in frame 2

    global category2
    global sort

    sort = False
    category2 = ''
    category_button2.config(text='Category', fg='blue', bg='yellow')

    refresh_table()


def sort_func():  # for the sort button in frame 2

    global sort
    global category2

    sort = True
    category_button2.config(text='Category', fg='blue', bg='yellow')
    refresh_table()
    category2 = ''


def delete_category_func():  # function for delete category button in settings

    global category3

    if category3 == '':
        tkinter.messagebox.showerror("Error", "Select a category")
    else:
        database.execute("DELETE FROM Categories WHERE CATEGORIES = ?", (category3,))
        connection.commit()

        category_button.menu.delete(category3)
        category_button2.menu.delete(category3)
        category_button3.menu.delete(category3)

        category3 = ''  # again assigning the default value
        status_bar2.config(text='Category deleted!')
        window.after(2000, clear_label)

    category_button3.config(text='Category', fg='blue', bg='yellow')


def add_category_func():  # function for add category button in settings

    status_bar2.config(text='Category added!')
    window.after(2000, clear_label)

    new_category = category_entry.get()
    if new_category == '':
        tkinter.messagebox.showerror('Error', 'Category cannot be empty')
    else:
        database.execute("INSERT INTO Categories VALUES(?)", (new_category,))
        connection.commit()
        database.execute("SELECT * FROM Categories")
        categories2 = database.fetchall()

        for entry in categories2:
            for name in entry:  # to assign the last entry in the category table to name
                pass
        category_button.menu.add_command(label=name, command=lambda name1=name: category_name(name1))  # python closure
        category_button2.menu.add_command(label=name, command=lambda name2=name: category_name2(name2))
        category_button3.menu.add_command(label=name, command=lambda name3=name: category_name3(name3))


def category_func():  # function for adding all the categories in the table

    for entry in categories:
        for name in entry:
            category_button.menu.add_command(label=name, command=lambda name1=name: category_name(name1))  # python closure
            category_button2.menu.add_command(label=name, command=lambda name2=name: category_name2(name2))
            category_button3.menu.add_command(label=name, command=lambda name3=name: category_name3(name3))


def set_budget_func():  # function for set button in settings

    budget = budget_entry.get()
    if budget == '' or any([a.isalpha() for a in str(budget)]) is True:  # if no budget is entered or is not number
        tkinter.messagebox.showerror(title='Error', message='Budget cannot be empty or non number')
    else:
        database.execute("INSERT INTO budget VALUES(?)", (budget,))
        connection.commit()
        month_exp_func()  # to change the budget label on frame 1

        status_bar2.config(text='Budget set!')
        window.after(2000, clear_label)


def refresh_plot():  # function for showing matplotlib graph

    exp = []
    date = []
    database.execute("SELECT * FROM expense_tracker")
    c = database.fetchall()
    day = 1
    for entry in c:
        if int(str(entry[5]).split('-')[1]) == datetime.datetime.now().month:  # if the month of entry is same as the current month
            day = int(str(entry[5]).split('-')[2])
            exp.append(entry[0])
            date.append(day)  # adding the date to the list

            break
    total = 0
    i = 0
    for entry in c:
        t_rupees = 0
        t_dollar = 0
        t_euros = 0
        if int(str(entry[5]).split('-')[1]) == datetime.datetime.now().month:
            day2 = int(str(entry[5]).split('-')[2])

            if entry[1] == "₹ INR":
                t_rupees = entry[0]
            elif entry[1] == "$ USD":
                t_dollar = entry[0]
            elif entry[1] == "€ EUR":
                t_euros = entry[0]

            if day2 != day:
                exp.append(total)
                date.append(day2)
                day = day2
                total = 0
                i += 1

            total = total + t_rupees + 75.98 * t_dollar + 83.29 * t_euros
            exp[i] = total

    print(exp)
    print(date)

    plt.plot(date, exp, marker='x')
    plt.xlabel("Date")
    plt.ylabel("Amount spent (Rs)")
    plt.show()


def show_label():  # function for showing label on the start frame and then unpacking the frame
    quote.config(text='“It isn\'t what you earn but how spend it that fixes your class.”')
    window.after(4000, lambda: frame(pack_frame=frame1))


# ------------------------------------------------------FOR START FRAME-----------------------------------------------#
window.after(2000, show_label)  # ***************************for start frame*********************************


# --------------------------------------------------------------------------------------------------------------------#


def add_new_to_table():  # function for adding a new expense to the expense report table
    database.execute("SELECT * FROM expense_tracker")
    c = database.fetchall()
    for entry in c:
        pass
    treev.insert("", 'end', text="L" + str(len(c)), values=entry)  # adding the last element in the treeview table

    database.execute("SELECT SUM(Expenses) FROM expense_tracker ")
    total = database.fetchone()

    total_label.config(text='Total expense = %.3f + ₹' % (total))  # to change the total label in the second frame


def refresh_table():  # function for refreshing thr expense report.
    date = date_ent.get_date()  # get date from the calendar

    if sort is False:  # if sort is false no sorting and showing all the expenses
        for a in treev.get_children():  # for deleting all the entries in the tree view table
            treev.delete(a)
        database.execute("SELECT * FROM expense_tracker")
        c = database.fetchall()
        j = 1
        for i in c:  # to insert all the entries from the database in the tree view table
            treev.insert("", 'end', text="L" + str(j),
                         values=i)
            j += 1
        # ------------------------------------to calculate total exp---------------------------------------------------#
        # for displaying total sum of expenses on the screen
        database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CURRENCY=?",
                         ('₹ INR',))

        t_rupees = database.fetchone()[0]
        if t_rupees is None:
            t_rupees = 0

        database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CURRENCY=?",
                         ('$ USD',))
        t_dollar = database.fetchone()[0]
        if t_dollar is None:
            t_dollar = 0
        database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CURRENCY=?",
                         ('€ EUR',))
        t_euros = database.fetchone()[0]
        if t_euros is None:
            t_euros = 0

        total = t_rupees + 75.98 * t_dollar + 83.29 * t_euros

        total_label.config(text='Total Expense : %.3f ₹' % (total))
        # -------------------------------------------------------------------------------------------------------------#
    else:  # if sort is false
        if status.get() == 1:  # if sort by category check box is checked
            if category2 == '':  # if no category is chosen
                tkinter.messagebox.showerror("Error", "Select a category")  # show error
            else:

                for a in treev.get_children():  # for deleting all the entries in the tree view table
                    treev.delete(a)
                database.execute("SELECT * FROM expense_tracker WHERE CATEGORY=?", (category2,))
                c = database.fetchall()
                j = 1
                for i in c:  # to insert all the entries from the database in the tree view table
                    treev.insert("", 'end', text="L" + str(j),
                                 values=i)
                    j += 1
                # ----------------------------------------------------------------------------------------------------#
                # ****************************************************************************************************#
                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CATEGORY=? AND CURRENCY=?",
                                 (category2, '₹ INR'))

                t_rupees = database.fetchone()[0]
                if t_rupees is None:
                    t_rupees = 0

                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CATEGORY=? AND CURRENCY=?",
                                 (category2, '$ USD'))
                t_dollar = database.fetchone()[0]
                if t_dollar is None:
                    t_dollar = 0
                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CATEGORY=? AND CURRENCY=?",
                                 (category2, '€ EUR'))
                t_euros = database.fetchone()[0]
                if t_euros is None:
                    t_euros = 0

                total = t_rupees + 75.98 * t_dollar + 83.29 * t_euros

                total_label.config(text='Total Expense : %.3f ₹' % (total))
                # ****************************************************************************************************#
                # ----------------------------------------------------------------------------------------------------#
        else:  # if sort by category is not checked

            if category2 == '':  # if no category is chosen i.e. sort by only date

                for a in treev.get_children():  # for deleting all the entries in the tree view table
                    treev.delete(a)
                database.execute("SELECT * FROM expense_tracker WHERE DATE=?", (str(date),))
                c = database.fetchall()
                j = 1
                for i in c:  # to insert all the entries from the database in the tree view table
                    treev.insert("", 'end', text="L" + str(j),
                                 values=i)
                    j += 1

                # ****************************************************************************************************#
                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CURRENCY=?",
                                 (str(date), '₹ INR'))

                t_rupees = database.fetchone()[0]
                if t_rupees is None:
                    t_rupees = 0

                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CURRENCY=?",
                                 (str(date), '$ USD'))
                t_dollar = database.fetchone()[0]
                if t_dollar is None:
                    t_dollar = 0
                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CURRENCY=?",
                                 (str(date), '€ EUR'))
                t_euros = database.fetchone()[0]
                if t_euros is None:
                    t_euros = 0

                total = t_rupees + 75.98 * t_dollar + 83.29 * t_euros

                total_label.config(text='Total Expense : %.3f ₹' % (total))

                # *****************************************************************************************************#
            else:  # if both date and category are chosen i.e. sort by both date and category

                for a in treev.get_children():  # for deleting all the entries in the tree view table
                    treev.delete(a)
                database.execute("SELECT * FROM expense_tracker WHERE DATE=? AND CATEGORY=?", (str(date), category2))
                c = database.fetchall()
                j = 1
                for i in c:  # to insert all the entries from the database in the tree view table
                    treev.insert("", 'end', text="L" + str(j),
                                 values=i)
                    j += 1
                # ****************************************************************************************************#
                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CATEGORY=? AND CURRENCY=?",
                                 (str(date), category2, '₹ INR'))

                t_rupees = database.fetchone()[0]
                if t_rupees is None:
                    t_rupees = 0

                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CATEGORY=? AND CURRENCY=?",
                                 (str(date), category2, '$ USD'))
                t_dollar = database.fetchone()[0]
                if t_dollar is None:
                    t_dollar = 0

                database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CATEGORY=? AND CURRENCY=?",
                                 (str(date), category2, '€ EUR'))
                t_euros = database.fetchone()[0]
                if t_euros is None:
                    t_euros = 0

                total = t_rupees + 75.98 * t_dollar + 83.29 * t_euros

                total_label.config(text='Total Expense : %.3f ₹' % (total))

            # ********************************************************************************************************#


m = 3  # for start_frame (different numbers for different frames)
# m = 0 for frame1, m = 1 for frame2, m = 2 for frame3

def frame(pack_frame):  # function for packing and unpacking frames

    global category2
    global category
    global currency
    global sort

    global m
    if m == 0:
        remove_frame = frame1
    elif m == 1:
        remove_frame = frame2
    elif m == 2:
        remove_frame = frame3

    else:
        remove_frame = start_frame

    if pack_frame == frame2:
        sort = False  # so that we do not get a sorted table
        refresh_table()  # for showing all the expenses
        m = 1
        category2 = ''  # setting the category to nothing
        category_button2.config(text='Category', fg='blue', bg='yellow')

    elif pack_frame == frame1:
        m = 0
        category = 'General'
        category_button.config(text='Category', fg='blue', bg='yellow')
        currency_button.config(text='Currency', fg='blue', bg='yellow')
    else:
        m = 2

    remove_frame.pack_forget()  # unpacking
    pack_frame.pack(expand=TRUE, fill='both')  # packing

    # for deleting a selected entry from the database


def delete_entry():  # function to delete a selected expense from expense report

    selected_item = treev.selection()  # returns a list containing a single id
    print(selected_item)
    value = treev.item(selected_item)['values']  # returns a list of values
    print(value)
    database.execute("""DELETE FROM expense_tracker WHERE
                                            Expenses=?
                                        AND CURRENCY=?
                                        AND CATEGORY=?
                                        AND MESSAGE=?
                                        AND TIME=?
                                        AND DATE=?""", (float(value[0]),
                                                        value[1],
                                                        value[2],
                                                        value[3],
                                                        value[4],
                                                        value[5]))
    connection.commit()  # saving changes in the database

    for i in selected_item:
        treev.delete(i)  # deleting the selected entry from the table

    # updating the labels on the first frame
    total_exp_func()
    today_exp_func()
    month_exp_func()

    # a second frame1 for displaying expenses
    # size of the frame1


# function to delete all expenses from the database
def delete_exp():  # function to delete all the expense from database

    answer = tkinter.messagebox.askquestion('Delete expenses', 'Are you sure?')  # a message box for confirming deletion
    if answer == 'yes':

        database.execute("DELETE FROM expense_tracker")
        connection.commit()

        refresh_table()  # refreshing the table after deleting all the entries

        # refreshing the labels on the first frame
        today_exp_func()
        total_exp_func()
        month_exp_func()

        status_bar['text'] = 'Expenses deleted!'
        frame1.after(2000, clear_label)
    else:
        pass


# to disappear the status label
def clear_label():  # to clear status bar from the screen
    status_bar['text'] = ''
    status_bar2.config(text='')


# function for adding expenses to the database
def add_to_db():  # to add an expense in the database

    global message
    global date_exp
    global time_exp

    exp = entry_exp.get()
    message = entry_message.get()
    date_exp = str(datetime.datetime.now().date())
    time_exp = str(datetime.datetime.now().time())

    if message == '':
        message = '-------------'

    if str(exp) == '' or any([a.isalpha() for a in str(exp)]) is True:
        tkinter.messagebox.showerror(title='Error', message='Expenses can only be numbers')

    else:
        database.execute("INSERT INTO expense_tracker VALUES(?,?,?,?,?,?)",
                         (exp, currency, category, message, str(time_exp)[:8], date_exp))
        connection.commit()

        add_new_to_table()
        today_exp_func()
        month_exp_func()
        total_exp_func()

        status_bar['text'] = 'Expense added!'  # for showing the label
        frame1.after(2000, clear_label)


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
def category_name3(name):  # to assign a category name (settings)
    global category3
    category3 = name
    category_button3.config(text=category3, bg='powder blue', fg='green')


def category_name2(name):  # to assign a category name (sort)
    global category2
    category2 = name
    category_button2.config(text=category2, bg='powder blue', fg='green')


# same as the currency_name
def category_name(name):  # to assign a category name (add)
    global category
    category = name
    category_button.config(text=category, bg='powder blue', fg='green')


# --------------------------------------------------------------------------------------------------------------------#

# for assigning name of the currency to a variable and displaying it on the menu button
def currency_name(name):  # to assign a currency name
    global currency
    currency = name
    currency_button.config(text=currency, bg='powder blue', fg='green')


# ---------------------------------------------------------------------------------------------------------------------#

# --------------------------------------------------------------------------------------------------------------------#
def month_exp_func():  # to calculate and print this month's expense on the screen
    database.execute("SELECT * FROM expense_tracker")
    c = database.fetchall()
    t_rupees, t_dollar, t_euros = 0, 0, 0

    for entry in c:
        if int(str(entry[5]).split('-')[1]) == datetime.datetime.now().month:  # if the month of an expense is same as the current month
            if entry[1] == "₹ INR":
                t_rupees += entry[0]
            elif entry[1] == "$ USD":
                t_dollar += entry[0]
            elif entry[1] == "€ EUR":
                t_euros += entry[0]

    month_exp = t_rupees + 75.98 * t_dollar + 83.29 * t_euros

    database.execute("SELECT * FROM budget")
    c = database.fetchall()
    if not c:  # if c is empty
        pass
    else:
        current_budget = c[len(c) - 1][0]  # the last entry
        if month_exp > current_budget:  # if monthly expense excedded the budget
            budgt_lbl.config(
                text='Expenses exceeded budget by {:.3f} ₹\n Budget = {} ₹'.format(month_exp - current_budget,
                                                                                   current_budget), fg='red')
        else:
            budgt_lbl.config(text='Maximum {:.3f} rupees to spend this month\n Budget = {} ₹'
                             .format(current_budget - month_exp, current_budget), fg='black')

    label_month.config(text="%.3f" % (month_exp) + ' ₹')


# ---------------------------------------------------------------------------------------------------------------------#
# function for calculating and displaying today's expenses on the screen
def today_exp_func():
    database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CURRENCY=?",
                     (str(datetime.datetime.now().date()), '₹ INR'))

    t_rupees = database.fetchone()[0]
    if t_rupees is None:
        t_rupees = 0

    database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CURRENCY=?",
                     (str(datetime.datetime.now().date()), '$ USD'))
    t_dollar = database.fetchone()[0]
    if t_dollar is None:
        t_dollar = 0
    database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE DATE=? AND CURRENCY=?",
                     (str(datetime.datetime.now().date()), '€ EUR'))
    t_euros = database.fetchone()[0]
    if t_euros is None:
        t_euros = 0

    total_today = t_rupees + 75.98 * t_dollar + 83.29 * t_euros

    label_today.config(text="%.3f" % (total_today) + ' ₹', fg='red')


# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#

# function for calculating and displaying total expense on the screen
def total_exp_func():
    database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CURRENCY=?",
                     ('₹ INR',))

    t_rupees = database.fetchone()[0]
    if t_rupees is None:
        t_rupees = 0

    database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CURRENCY=?",
                     ('$ USD',))
    t_dollar = database.fetchone()[0]
    if t_dollar is None:
        t_dollar = 0
    database.execute("SELECT SUM(Expenses) FROM expense_tracker WHERE CURRENCY=?",
                     ('€ EUR',))
    t_euros = database.fetchone()[0]
    if t_euros is None:
        t_euros = 0

    total_all = t_rupees + 75.98 * t_dollar + 83.29 * t_euros

    label_total.config(text="%.3f" % (total_all) + ' ₹', fg='red')


# -----------------------------------------------------------frame1----------------------------------------------------#
# -------------------------------------------------------Labels--------------------------------------------------------#

head_label = Label(frame1, text='EXPENSE TRACKER', fg='blue', bg='pale turquoise', font=font.Font(size=60))
head_label.pack(fill=X)

category_label = Label(frame1, text='Select category', font=font2, fg='blue')
category_label.place(x=725, y=140)

entry_label = Label(frame1, text='Enter expense', font=font2, fg='blue')
entry_label.place(x=100, y=140)

currency_label = Label(frame1, text='Select currency', font=font2, fg='blue')
currency_label.place(x=725, y=200)

message_label = Label(frame1, text='Enter message', font=font2, fg='blue')
message_label.place(x=100, y=200)

today_exp = Label(frame1, text='Today\'s expenses', fg='blue', font=font3)
today_exp.place(x=100, y=400)

month_exp_l = Label(frame1, text='This month\'s expense', fg='blue', font=font3)
month_exp_l.place(x=34, y=500)
total_exp = Label(frame1, text='Total expense', fg='blue', font=font3)  # label for total expenses
total_exp.place(x=165, y=600)

label_month = Label(frame1, fg='green4', font=font3)  # label for month expense
label_today = Label(frame1, fg = 'green4', font=font3)  # label for today's expense
label_total = Label(frame1, fg = 'green4', font=font3)

status_bar = Label(frame1, font=font.Font(size=15), relief=SUNKEN, bd=1, anchor=W, fg='red')  # for giving status
status_bar.pack(side=BOTTOM, fill=X)

budgt_lbl = Label(frame1, font=font2, bd=1, relief=SUNKEN)
budgt_lbl.place(x=900, y=500)

# ----------------------------------------------------Entry-----------------------------------------------------------#
entry_exp = Entry(frame1, font=font2, bg='light cyan', fg='blue')  # entry of expense
entry_exp.place(x=300, y=140)
entry_message = Entry(frame1, font=font2, bg='light cyan', fg='blue')  # entry for message
entry_message.place(x=300, y=200)

message = entry_message.get()  # it will fetch what is written on the screen
date_exp = str(datetime.datetime.now().date())  # it will give today's date
time_exp = str(datetime.datetime.now().time())  # it will give current time

# ---------------------------------------------------buttons----------------------------------------------------------#
# button for adding expense to the database

photo2 = PhotoImage(file=r"unnamed.png")
photoimage = photo2.subsample(10, 10)

add_exp = Button(frame1, text=' Add expense', image=photoimage, fg='blue', bg='powder blue', command=add_to_db, font=font2,
                 compound=LEFT)
add_exp.place(x=100, y=300)
# ------------------------------------------------
database.execute("SELECT * FROM Categories")
categories = database.fetchall()
# -------------------------------------------------

# menu button for selecting   category

category_button = Menubutton(frame1, text='Category', fg='blue', bg='light cyan', font=font2, relief=RIDGE)
category_button.menu = Menu(category_button, font=font2)
category_button['menu'] = category_button.menu
category_button.place(x=950, y=140)

# menu for selecting a currency
currency_button = Menubutton(frame1, text='Currency', bg='light cyan', fg='blue', font=font2, relief=RIDGE)
currency_button.menu = Menu(currency_button, font=font2)
currency_button['menu'] = currency_button.menu
currency_button.menu.add_command(label='₹ Rupee', command=lambda: currency_name('₹ INR'))
currency_button.menu.add_command(label='$ Dollar', command=lambda: currency_name('$ USD'))
currency_button.menu.add_command(label='€ Euro', command=lambda: currency_name('€ EUR'))
currency_button.place(x=950, y=200)

# button to delete all the expenses
delete_button = Button(frame1, text='Delete all expenses', fg='blue', bg='powder blue', image=photo3, command=delete_exp,
                       font=font2, compound=LEFT)
delete_button.place(x=800, y=300)
# ---------------------------------------------------------------------------------------Photos-----------------------#
settings_photo = settings_photo.subsample(15, 15)
report_photo = report_photo.subsample(15, 15)
graph_photo = graph_photo.subsample(15, 15)
exit_photo1 = exit_photo.subsample(22, 22)
exit_photo2 = exit_photo.subsample(7, 7)

# ------------------------------------------------------------MENU-----------------------------------------------------#
# menu for exit or view expense
menu1 = Menu(window)
window.config(menu=menu1)
subMenu = Menu(menu1)
menu1.add_cascade(label='File', menu=subMenu, font=font.Font(size=15))
subMenu.add_command(label='Expense report', image=report_photo, compound=LEFT, font=font.Font(size=15),
                    command=lambda: frame(pack_frame=frame2))
subMenu.add_command(label='View Graph', image=graph_photo, compound=LEFT, font=font.Font(size=15), command=refresh_plot)
subMenu.add_command(label='Settings', font=font.Font(size=15), image=settings_photo,
                    compound=LEFT, command=lambda: frame(pack_frame=frame3))
subMenu.add_command(label='Exit', image=exit_photo1, compound=LEFT, font=font.Font(size=15), command=window.quit)

# to exit from the frame1
exit_button = Button(frame1, text=' Exit App', image=exit_photo2, compound=LEFT, font=font.Font(size=30), fg='red',
                     bg='pink',
                     command=window.quit)
exit_button.pack(side=BOTTOM)

# ---------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------frame2-----------------------------------------------------------#
main_page_button = Button(frame2, text='Go to main page', font=font2, fg='blue', bg='powder blue',
                          command=lambda: frame(pack_frame=frame1))
main_page_button.place(x=1100, y=600)
delete_button2 = Button(frame2, text='Delete selected expense', fg='red', bg='pink', command=delete_entry,
                        image=photo3, compound=LEFT,
                        font=font2)  # delete  button
delete_button2.place(x=1100, y=65)

treev = ttk.Treeview(frame2, selectmode='browse')  # tree view table for displaying all the expenses on the screen
treev.place(x=10, y=60)
treev["columns"] = ("1", "2", "3", "4", "5", "6")
treev['show'] = 'headings'
treev.column("1", width=150, anchor='c')
treev.column("2", width=150, anchor='c')
treev.column("3", width=150, anchor='c')
treev.column("4", width=150, anchor='c')
treev.column("5", width=150, anchor='c')
treev.column("6", width=150, anchor='c')

verscrlbar = ttk.Scrollbar(frame2,
                           orient="vertical",
                           command=treev.yview)

# Calling pack method w.r.to verical
# scrollbar
verscrlbar.place(x=0, y=150)

# Configuring tree view
treev.configure(xscrollcommand=verscrlbar.set)

treev.heading("1", text="Expenses")
treev.heading("2", text="Currency")
treev.heading("3", text="Category")
treev.heading("4", text="Message")
treev.heading("5", text="Time")
treev.heading("6", text="Date")

head_label2 = Label(frame2, text='EXPENSE REPORTS', fg='white', bg='blue', font=font3)
head_label2.pack(side=TOP, fill=X)

total_label = Label(frame2, fg='red', font=font2)
total_label.place(x=600, y=300)

date_ent = DateEntry(frame2, text='Select date', width=15, bg='blue', font=font2, fg='white', borderwidth=3)
date_ent.place(x=100, y=400)

sort_label = Label(frame2, text='Filter Expenses', font=font2, fg='blue')
sort_label.place(x=230, y=350)

sort_button = Button(frame2, text='Filter', fg='white', bg='blue', font=font2, command=sort_func)
sort_button.place(x=220, y=500)

refresh_button = Button(frame2, text='Refresh', fg='blue', bg='powder blue', font=font2, command=refresh_func)
refresh_button.place(x=1100, y=300)

category_button2 = Menubutton(frame2, text='Category', fg='blue', bg='light cyan', font=font2, relief=RIDGE)
category_button2.menu = Menu(category_button2, font=font2)
category_button2['menu'] = category_button2.menu
category_button2.place(x=400, y=400)

check_button = Checkbutton(frame2, text='Filter by category only', variable=status, font=font2)
check_button.place(x=100, y=600)

refresh_table()  # *************************** FOR REFRESHING THE EXPENSE REPORT **********************************

# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------------frame3---------------------------------------------------------#
settings_label = Label(frame3, text='SETTINGS', font=font2, bg='blue', fg='white')
settings_label.pack(fill=X)

set_budget = Button(frame3, text='SET', font=font2, bg='powder blue', fg='blue', command=set_budget_func)
set_budget.place(x=300, y=230)

budget_label = Label(frame3, text='Set Monthly budget\n in rupees', font=font2, fg='blue')
budget_label.place(x=100, y=150)

budget_entry = Entry(frame3, font=font2, bg='light cyan', fg='blue')
budget_entry.place(x=380, y=150)

add_category_label = Label(frame3, text='Add category', fg='blue', font=font2)
add_category_label.place(x=850, y=150)

category_entry = Entry(frame3, fg='blue', bg='light cyan', font=font2)
category_entry.place(x=1050, y=150)

add_photo = add_photo.subsample(10, 10)
category_add = Button(frame3, text=' Add Category', image=add_photo, compound=LEFT, fg='blue', bg='powder blue', font=font2,
                      command=add_category_func)
category_add.place(x=900, y=230)

main_page_button2 = Button(frame3, text='Go to main page', font=font2, fg='blue', bg='powder blue',
                           command=lambda: frame(pack_frame=frame1))
main_page_button2.place(x=1100, y=600)

status_bar2 = Label(frame3, text='', font=font.Font(size=15), fg='red', bd=1, relief=SUNKEN, anchor=W)
status_bar2.pack(side=BOTTOM, fill=X)

delete_label = Label(frame3, text='Delete category', fg='blue', font=font2)
delete_label.place(x=150, y=400)

category_button3 = Menubutton(frame3, text='Category', fg='blue', bg='light cyan', font=font2, relief=RIDGE)
category_button3.menu = Menu(category_button3, font=font2)
category_button3['menu'] = category_button3.menu

# add all the categories in the table to the menu buttons
category_func()  # ****************************function for all three categories***************************************

category_button3.place(x=400, y=400)

delete_category = Button(frame3, text=' Delete category', fg='blue', bg='powder blue', font=font2, image=photo3,
                         compound=LEFT, command=delete_category_func)
delete_category.place(x=225, y=475)

# -----------------------------------------------------Expenses--------------------------------------------------------#
today_exp_func()  # for refreshing today's expense at the time of start
total_exp_func()  # for refreshing total expense at the time of start
month_exp_func()  # for refreshing monthly expense at the time of start
# ---------------------------------------------------------------------------------------------------------------------#
label_today.place(x=450, y=400)  # it will print total expense on the screen
label_month.place(x=450, y=500)  # it will print month's expense on the screen
label_total.place(x=450, y=600)  # it will print today's expenses on the screen
# ---------------------------------------------------------------------------------------------------------------------#
window.mainloop()  # keeping the frame1 in an infinite loop

# finally closing the database and the connection
database.close()
connection.close()
# ---------------------------------------------------------THE END-----------------------------------------------------#
