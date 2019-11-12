from tkinter import *
from tkinter import ttk
import mysql.connector as conn
from tkinter import messagebox as msg_box


def add_info():
    try:
        std_id = int(entry_id.get())
        f_name = entry_f_name.get()
        l_name = entry_l_name.get()
        st_address = entry_st_address.get()
        st_number = entry_st_number.get()
        st_degree = entry_st_degree.get()

        query = 'insert into entry(id, f_name, l_name, st_address, st_number, st_degree) values(%s, %s, %s, %s, %s, %s)'
        values = (std_id, f_name, l_name, st_address, st_number, st_degree)
        db_cursor.execute(query, values)
        msg_box.showinfo("Data inserted successfully.")
        connector.commit()
        clear()
        show()

    except ValueError as error:
        print(error)

    except conn.IntegrityError as error:
        print(error)


def clear():
    entry_id.config(state='normal')
    entry_search.delete(0, END)
    entry_id.delete(0, END)
    entry_f_name.delete(0, END)
    entry_l_name.delete(0, END)
    entry_st_address.delete(0, END)
    entry_st_number.delete(0, END)
    entry_st_degree.delete(0, END)


def show():
    records = student_table.get_children()

    for element in records:
        student_table.delete(element)

    query = 'select * from entry'
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    for row in results:
        student_table.insert('', 'end', values=row)


def search():
    values = (combo_search.get(), entry_search.get())
    query = "select * from entry where " + "%s" % values[0] + " like '%" + "%s" % values[1] + "%'"
    db_cursor.execute(query)

    records = student_table.get_children()

    for element in records:
        student_table.delete(element)

    results = db_cursor.fetchall()
    for row in results:
        student_table.insert('', 'end', values=row)


def update():
    try:
        f_name = entry_f_name.get()
        l_name = entry_l_name.get()
        st_address = entry_st_address.get()
        st_number = entry_st_number.get()
        st_degree = entry_st_degree.get()

        query = 'update entry set f_name=%s, l_name=%s, st_address=%s, st_number=%s, st_degree=%s where id=%s'
        values = (f_name, l_name, st_address, st_number, st_degree, pointer())
        db_cursor.execute(query, values)
        connector.commit()
        clear()
        show()

    except ValueError as error:
        print(error)


def delete():
    query = 'delete from entry where id=%s'
    values = (pointer(),)
    db_cursor.execute(query, values)
    connector.commit()
    show()
    clear()


def pointer():
    try:
        clear()
        point = student_table.focus()
        content = student_table.item(point)
        row = content['values']
        entry_id.insert(0, row[0])
        entry_f_name.insert(0, row[1])
        entry_l_name.insert(0, row[2])
        entry_st_address.insert(0, row[3])
        entry_st_number.insert(0, row[4])
        entry_st_degree.insert(0, row[5])
        return row[0]

    except IndexError:
        pass


try:
    connector = conn.connect(user='root', passwd='sameasbefore', host='localhost', database='management_sys')
    db_cursor = connector.cursor()
    db_cursor.execute('create table if not exists entry(id int not null,'
                      'f_name varchar(40), l_name varchar(40), st_address varchar(50), st_number varchar(13), st_degree varchar(40),'
                      'constraint pk_id primary key(id))')

except conn.DatabaseError as error:
    print(error)

root = Tk()
root.title("Student Management System")
root.geometry('700x610+300+50')
root.configure(bg="light blue")

# ------------- Frames -------------
top_frame = Frame(root)
top_frame.configure(bg="light blue")
top_frame.pack()

bottom_frame = Frame(root)
bottom_frame.configure(bg="light blue")
bottom_frame.pack()

show_frame = Frame(root, width=200, height=100, relief=RIDGE, bd=4)
show_frame.configure(bg="light blue")
show_frame.pack()

lbl_search_by = Label(top_frame, text="Search By", font='TimesNewRoman 11', bg='light blue')
lbl_search_by.grid(row=0, column=0, padx=15, pady=8)

combo_search = ttk.Combobox(top_frame, width=28, font='arial 12')
combo_search['values'] = ('Id', 'First Name', 'Last Name', 'Address', 'Number', 'Degree')
combo_search.current(0)
combo_search.grid(row=0, column=1, padx=15, pady=8)

# Adding widgets in the form
lbl_search = Label(top_frame, text="Search", font='TimesNewRoman 11', bg='light blue')
lbl_id = Label(top_frame, text="ID", font='TimesNewRoman 11', bg='light blue')
lbl_f_name = Label(top_frame, text="First Name", font='TimesNewRoman 11', bg='light blue')
lbl_l_name = Label(top_frame, text="Last Name", font='TimesNewRoman 11', bg='light blue')
lbl_address = Label(top_frame, text="Address", font='TimesNewRoman 11', bg='light blue')
lbl_number = Label(top_frame, text="Number", font='TimesNewRoman 11', bg='light blue')
lbl_degree = Label(top_frame, text="Degree", font='TimesNewRoman 11', bg='light blue')

lbl_search.grid(row=1, column=0, padx=15, pady=8)

entry_search = Entry(top_frame, width=28, font='arial 11')
entry_search.grid(row=1, column=1, padx=15, pady=8)
btn_search = Button(top_frame, width=8, text='Search', font='TimesNewRoman 11', command=search)
btn_search.grid(row=2, column=1, padx=20, pady=20)

lbl_id.grid(row=3, column=0, padx=15, pady=8)
lbl_f_name.grid(row=4, column=0, padx=15, pady=8)
lbl_l_name.grid(row=5, column=0, padx=15, pady=8)
lbl_address.grid(row=6, column=0, padx=15, pady=8)
lbl_number.grid(row=7, column=0, padx=15, pady=8)
lbl_degree.grid(row=8, column=0, padx=15, pady=8)

# ---------------- Entry of the form ----------------

entry_id = Entry(top_frame, width=28, font='arial 11')
entry_f_name = Entry(top_frame, width=28, font='arial 11')
entry_l_name = Entry(top_frame, width=28, font='arial 11')
entry_st_address = Entry(top_frame, width=28, font='arial 11')
entry_st_number = Entry(top_frame, width=28, font='arial 11')
entry_st_degree = Entry(top_frame, width=28, font='arial 11')

entry_search.bind('<Return>', lambda e: search())

entry_id.grid(row=3, column=1, padx=15, pady=8)
entry_f_name.grid(row=4, column=1, padx=15, pady=8)
entry_l_name.grid(row=5, column=1, padx=15, pady=8)
entry_st_address.grid(row=6, column=1, padx=15, pady=8)
entry_st_number.grid(row=7, column=1, padx=15, pady=8)
entry_st_degree.grid(row=8, column=1, padx=15, pady=8)

# ---------------- Button Add -------------------
btn_add = Button(bottom_frame, width=8, text='Add', font='TimesNewRoman 11', command=add_info)
btn_show = Button(bottom_frame, width=8, text='Show', font='TimesNewRoman 11', command=show)
btn_delete = Button(bottom_frame, width=8, text='Delete', font='TimesNewRoman 11', command=delete)
btn_update = Button(bottom_frame, width=8, text='Update', font='TimesNewRoman 11', command=update)
btn_clear = Button(bottom_frame, width=8, text='Clear', font='TimesNewRoman 11', command=clear)


btn_add.grid(row=9, column=0, padx=20, pady=20)
btn_show.grid(row=9, column=1, padx=20, pady=20)
btn_delete.grid(row=9, column=2, padx=20, pady=20)
btn_update.grid(row=9, column=3, padx=20, pady=20)
btn_clear.grid(row=9, column=4, padx=20, pady=20)

# ------------ Tree view ------------------
scroll_x = Scrollbar(show_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(show_frame, orient=VERTICAL)

student_table = ttk.Treeview(show_frame, column=('id', 'f_name', 'l_name', 'st_address', 'st_number', 'st_degree'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
student_table.pack()

student_table.column('id', width=120)
student_table.column('f_name', width=120)
student_table.column('l_name', width=120)
student_table.column('st_address', width=120)
student_table.column('st_number', width=120)
student_table.column('st_degree', width=120)
student_table['show'] = 'headings'

student_table.heading('id', text='ID')
student_table.heading('f_name', text='First Name')
student_table.heading('l_name', text='Last Name')
student_table.heading('st_address', text='Address')
student_table.heading('st_number', text='Number')
student_table.heading('st_degree', text='Degree')

scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)
student_table.bind('<ButtonRelease-1>', lambda e: pointer())

root.mainloop()