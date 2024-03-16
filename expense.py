import datetime
import sqlite3
from tkcalendar import DateEntry

from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

connector = sqlite3.connect("expenseproject.db")
cursor = connector.cursor()

connector.execute(
	'CREATE TABLE IF NOT EXISTS Tracker1 (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Name TEXT, Kind  TEXT, Cash FLOAT, ModeOfPayment TEXT)'
)
connector.commit()

def clear_fields():
	global kind, name, amnt, MoP, date, table,expen1

	today_date = datetime.datetime.now().date()

	kind.set('') ; name.set('') ; amnt.set(0.0) ; MoP.set('Cash'), date.set_date(today_date)
	table.selection_remove(*table.selection())
	#expense.set(expen1)
	
def list_all_expenses():
	global connector, table

	table.delete(*table.get_children())

	all_data = connector.execute('SELECT * FROM Tracker1')
	data = all_data.fetchall()

	


	for values in data:
		table.insert('', END, values=values)

	
def view_expense_details():
	global table
	global date, name, kind, amnt, MoP

	if not table.selection():
		mb.showerror('No expense selected', 'Please select an expense from the table to view its details')

	current_selected_expense = table.item(table.focus())
	values = current_selected_expense['values']

	expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))

	date.set_date(expenditure_date) ; name.set(values[2]) ; kind.set(values[3]) ; amnt.set(values[4]) ; MoP.set(values[5])


def expense_details():
	global table
	global income,expense,expen1
	global connector

	expen = connector.execute('SELECT Cash FROM Tracker1')
	data1 = expen.fetchall()
	totalexpense=0
	data2=[]

	for i in data1:
		for j in i:
			data2.append(j)

	for exp in range(0,len(data2)):
			totalexpense=totalexpense+data2[exp]

	expense.set(totalexpense)
	data3=income.get()

	if not income.get():
		mb.showerror( "Please enter all the income amount")
	else:
		if data3>totalexpense:
			mb.showinfo("Personal expense Tracker","YOUR EXPENSE IS LESSTHAN YOUR INCOME")
		else:
			mb.showinfo("Personal expense Tracker","YOUR EXPENSE IS MORETHAN YOUR INCOME")

	clear_fields()


def add_another_expense():
	global date, name, kind, amnt, MoP
	global connector

	if not date.get() or not name.get() or not kind.get() or not amnt.get() or not MoP.get():
		mb.showerror( "Please enter all the missing fields")
	else:
		connector.execute(
		'INSERT INTO Tracker1 (Date, Name, Kind, Cash, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
		(date.get_date(), name.get(), kind.get(), amnt.get(), MoP.get())
		)
		connector.commit()

		clear_fields()
		list_all_expenses()
		mb.showinfo('ExpensTracker',"Users expense added")

def edit_expense():
	global table

	def edit_existing_expense():
		global date, amnt, kind, name, MoP
		global connector, table

		current_selected_expense = table.item(table.focus())
		contents = current_selected_expense['values']

		connector.execute('UPDATE Tracker1 SET Date = ?, Name = ?,  Kind = ?, Cash = ?, ModeOfPayment = ? WHERE ID = ?',
		                  (date.get_date(), name.get(), kind.get(), amnt.get(), MoP.get(), contents[0]))
		connector.commit()

		clear_fields()
		list_all_expenses()

		mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
		edit_btn.destroy()
		return

	if not table.selection():
		mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
		return

	view_expense_details()

	edit_btn = Button(root, text='Edit expense', width=30, command=edit_existing_expense)
	edit_btn.place(x=10, y=395)
	

def remove_expense():
	if not table.selection():
		mb.showerror('No record selected!', 'Please select a record to delete!')
		return

	current_selected_expense = table.item(table.focus())
	values_selected = current_selected_expense['values']

	surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')

	if surety:
		connector.execute('DELETE FROM Tracker1 WHERE ID=%d' % values_selected[0])
		connector.commit()

		list_all_expenses()
		mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')


def remove_all_expenses():
	surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')

	if surety:
		table.delete(*table.get_children())

		connector.execute('DELETE FROM Tracker1')
		connector.commit()

		clear_fields()
		list_all_expenses()
		mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
	else:
		mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')









root = Tk()
root.title('Personal Expense Tracker')
root.geometry('1200x550')
root.config(bg='#4a7a8c')



Label(root, text='PERSONAL EXPENSE TRACKER', font=('Noto Sans CJK TC', 15, 'bold')).pack(side=TOP, fill=X)

kind = StringVar()
amnt = DoubleVar()
name = StringVar()
MoP = StringVar(value='Cash')
income=DoubleVar()
expense=DoubleVar()
expen1=DoubleVar()


Label(root, text='Date (M/DD/YY)   ').place(x=10, y=50)
date = DateEntry(root, date=datetime.datetime.now().date())
date.place(x=160, y=50)

Label(root, text='Name\t             ').place(x=10, y=230)
Entry(root, width=31, text=name).place(x=10, y=260)

Label(root, text='kind of expense           ').place(x=10, y=100)
Entry(root, width=31, text=kind).place(x=10, y=130)

Label(root, text='Cash\t             ').place(x=10, y=180)
Entry(root, width=14, text=amnt).place(x=160, y=180)

Label(root, text='Mode of Payment  ',).place(x=10, y=310)
dd1 = OptionMenu(root, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay'])
dd1.place(x=160, y=305)     ;     dd1.configure(width=10)

Label(root,text='Income          ').place(x=10,y=350)
Entry(root,width=20,text=income).place(x=160,y=350)

Button(root, text='Add expense', width=30,command=add_another_expense).place(x=10, y=395)
Button(root,text='view expense details',width=30,command=expense_details).place(x=10,y=450)

Button(root, text='Delete Expense', width=25,command=remove_expense).place(x=350, y=50)# 

Button(root, text='Clear Feilds', width=25,command=clear_fields).place(x=550, y=50)#

Button(root, text='Delete All Expenses', width=25,command=remove_all_expenses).place(x=750, y=50)#

Button(root, text='View Selected Expense\'s Details',command=view_expense_details, width=25).place(x=450, y=80)

Button(root, text='Edit Selected Expense',   width=25,command=edit_expense,).place(x=650,y=80)#

Label(root, text='Toal expense       ').place(x=750,y=120)
Entry(root,width=30,text=expense).place(x=850,y=120)

#TREE VIEW widget
tree_frame = Frame(root)
tree_frame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)

table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Name', 'Kind of expense', 'Cash', 'Mode of Payment'))

X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='S No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Name', text='Name', anchor=CENTER)
table.heading('Kind of expense', text='Kind of expense', anchor=CENTER)
table.heading('Cash', text='Cash', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=95, stretch=NO)  # Date column
table.column('#3', width=150, stretch=NO)  # Payee column
table.column('#4', width=325, stretch=NO)  # Title column
table.column('#5', width=135, stretch=NO)  # Amount column
table.column('#6', width=125, stretch=NO)  # Mode of Payment column

table.place(relx=0, y=0, relheight=1, relwidth=1)







list_all_expenses()

root.mainloop()