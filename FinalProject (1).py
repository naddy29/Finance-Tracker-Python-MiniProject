import tkinter as tk
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
import requests
from PIL import Image, ImageTk

# Function to add an expense to the list and save it to a CSV file
def add_expense():
    category = category_dropdown.get()
    description = description_entry.get()
    amount = amount_entry.get()

    if category and description and amount:
        current_date = datetime.now().strftime("%Y-%m-%d")
        row_data = [current_date, category, description, amount]

        expenses_tree.insert('', tk.END, values=row_data, tags=('lavender',))
        
        category_dropdown.set("")  # Clear the category selection
        description_entry.delete(0, tk.END)  # Clear the name entry
        amount_entry.delete(0, tk.END)

        # Append the expense data to the expenses list
        expenses_data.append(row_data)
        save_to_csv()  # Save the data to the CSV file

    else:
        messagebox.showinfo("Please fill out all the fields!")


def save_expenses():
    current_date = datetime.now().strftime("%Y-%m-%d")
    today_expenses = [row for row in expenses_data if row[0] == current_date]
    if today_expenses:
        with open("expenses_today.csv", mode="w", newline='') as csv_file:
            fieldnames = ["Date", "Category", "Name", "Amount"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for row in today_expenses:
                csv_writer.writerow({"Date": row[0], "Category": row[1], "Name": row[2], "Amount": row[3]})

        # Display a message box
        messagebox.showinfo("Expenses Saved", "Expenses for today have been saved.")

    # Clear the table
    #refresh_table()

"""def refresh_table():
    for row in expenses_tree.get_children():
        expenses_tree.delete(row)

    for row in expenses_data:
        expenses_tree.insert('', tk.END, values=row, tags=('lavender',))"""

# Function to show the pie chart with a legend
def update_pie_chart():
    show_pie_chart()
    window.after(3000, update_pie_chart)  # Update every 3 seconds (3000 milliseconds)

# Function to show the pie chart with a legend
def show_pie_chart():
    category_amount = {}  # Dictionary to store category-wise expenses
    for row in expenses_data:
        category, name, amount = row[1], row[2], float(row[3])
        if category in category_amount:
            category_amount[category] += amount
        else:
            category_amount[category] = amount

    categories = list(category_amount.keys())
    amounts = list(category_amount.values())

    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)
    wedges, texts, autotexts = ax.pie(
        amounts,
        labels=len(categories) * [''],  # Set labels to empty strings
        autopct='',
        startangle=140,
        textprops={'color': "white"}  # Set text color to white
    )
    ax.set_title("Expense Distribution")

    # Add a legend
    ax.legend(wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    pie_chart = FigureCanvasTkAgg(fig, add_expenses_tab)
    pie_chart.get_tk_widget().place(x=0, y=500, width=500, height=295)


# Function to update the line graph
def update_line_graph():
    show_line_graph()  # Update the line graph
    window.after(3000, update_line_graph)  # Update every 3 seconds (3000 milliseconds)


def show_line_graph():
    date_expenses = {}  # Dictionary to store date-wise expenses
    for row in expenses_data:
        date, category, amount = row[0], row[2], float(row[3])
        if date in date_expenses:
            date_expenses[date] += amount
        else:
            date_expenses[date] = amount

    dates = list(date_expenses.keys())
    expenses = list(date_expenses.values())

    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(dates, expenses, marker='o', linestyle='-')
    ax.set_xlabel("Dates")
    ax.set_ylabel("Expenses")
    ax.set_title("Expense Over Time")

    line_chart = FigureCanvasTkAgg(fig, add_expenses_tab)
    line_chart.get_tk_widget().place(x=650, y=450, width=650, height=380)

def delete():
    selected_item = expenses_tree.selection()
    if selected_item:
        # Get the index of the selected item and delete it from the Treeview
        index = expenses_tree.index(selected_item)
        expenses_tree.delete(selected_item)

        # Update the expenses_data list by removing the deleted item
        del expenses_data[index]

        # Save the updated data to the CSV file
        save_to_csv()


def save_to_csv():
    with open("expenses.csv", mode="w", newline='') as csv_file:
        fieldnames = ["Date", "Category", "Description", "Amount"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for row in expenses_data:
            csv_writer.writerow({"Date": row[0], "Category": row[1], "Description": row[2], "Amount": row[3]})


def add_friend_expense():
    friend = friend_var.get()
    category1 = category1_var.get()
    amount1 = amount1_var.get()

    if friend and category1 and amount1:
        current_date = datetime.now().strftime("%Y-%m-%d")
        row_data = [current_date, friend, category1, amount1]

        friend_expenses_tree.insert('', tk.END, values=row_data, tags=('lavender',))
        
        friend_var.set("")     # Clear the friend entry
        category1_var.set("")   # Clear the category selection
        amount1_var.set("")     # Clear the amount entry

        # Append the friend expense data to the list
        friend_expenses_data.append(row_data)
        save_to_csv()

currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "INR"]
def convert_currency():
    amount2 = float(amount2_entry.get())
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    
    # Check if the currencies are different
    if from_currency != to_currency:
        try:
            # Fetch exchange rate from a currency conversion API
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            exchange_rate = data["rates"][to_currency]
            
            # Perform the conversion
            converted_amount = amount2 * exchange_rate
            result_label.config(text=f"{amount2} {from_currency} = {converted_amount:.2f} {to_currency}")

        except Exception as e:
            result_label.config(text="Error fetching data")
    else:
        result_label.config(text="Currencies are the same")
        
# Create the main application window
window = tk.Tk()
window.geometry("1302x1192")
window.configure(bg="#FFFFFF")
window.title("Expense Tracker")

# Create a Notebook widget for different tabs
notebook = ttk.Notebook(window)
notebook.place(x=0, y=0, relwidth=3, relheight=2)

# Create a tab for "Home"
home_tab = tk.Frame(notebook, bg="white")
notebook.add(home_tab, text="Home")

# Create a tab for "Add Expenses"
add_expenses_tab = tk.Frame(notebook, bg="white")
notebook.add(add_expenses_tab, text="Add Expenses")

friends_tab = tk.Frame(notebook, bg="white")
notebook.add(friends_tab, text="Friends")

currency_converter_tab =tk.Frame(notebook, bg="white")
notebook.add(currency_converter_tab, text= "Currency Conversion")

# Create a Treeview widget to display expenses in rows and columns
expenses_tree = ttk.Treeview(add_expenses_tab, columns=("Date", "Category", "Description", "Amount"), show="headings", style="mystyle.Treeview")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Description", text="Description")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.pack()
expenses_tree.place(x=450, y=43, width=884, height=395)

# Create a style for the Treeview widget
expenses_style = ttk.Style()
expenses_style.theme_use("alt")
expenses_style.configure("Treeview",
                background="#E6E6FA",
                foreground="black",
                rowheight="25",
                fieldbackground="#E6E6FA")

# Tag all rows with "lavender" background color
expenses_tree.tag_configure("lavender", background="#E6E6FA")

# Create and pack the "Category" label and dropdown with scrollbar
category_label = tk.Label(add_expenses_tab, text="Category:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
category_label.place(x=64.0, y=43.0)
categories = ["Food", "Home", "Transport", "Shopping","Others"]
#category_var = tk.StringVar()
category_dropdown = ttk.Combobox(add_expenses_tab, values=categories)
category_dropdown.place(x=64.0, y=73.0, width=260.0, height=35.0)

# Create and pack the "Name" label with colored background
description_label = tk.Label(add_expenses_tab, text="Description:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
description_label.place(x=64.0, y=120.0)
#description_var = tk.StringVar()
description_entry = tk.Entry(add_expenses_tab, bd=1, highlightthickness=1, bg="#FFFFFF", fg="#000000")
description_entry.place(x=64.0, y=150.0, width=260.0, height=35.0)

# Create and pack the "Amount" label with a colored background
amount_label = tk.Label(add_expenses_tab, text="Amount:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
amount_label.place(x=64.0, y=197.0)
amount_entry = tk.Entry(add_expenses_tab, bd=1, highlightthickness=1, bg="#FFFFFF", fg="#000000")
amount_entry.place(x=64.0, y=227.0, width=260.0, height=35.0)

# Create and pack the "Add Expense" button
add_button = tk.Button(
    add_expenses_tab,
    text="Add Expense",
    command=add_expense,
    font=("Inter ExtraBold", 16),
    bg="#E0D7FF",
    fg="#000000",
    bd=1, highlightthickness=1,
)
add_button.place(x=64.0, y=285.0, width=260, height=50)

save_button = tk.Button(
    add_expenses_tab,
    text="Save",
    command=save_expenses,
    font=("Inter ExtraBold", 16),
    bg="#E0D7FF",
    fg="#000000",
    bd=1, highlightthickness=1,
)
save_button.place(x=64.0, y=345.0, width=260, height=50)

delete_button = tk.Button(
    add_expenses_tab,
    text="Delete selected",
    command=delete,
    font=("Inter ExtraBold", 16),
    bg="#E0D7FF",
    fg="#000000",
    bd=1, highlightthickness=1,
)
delete_button.place(x=64.0, y=405.0, width=260, height=50)

friend_expenses_tree = ttk.Treeview(friends_tab, columns=("Date","Friend", "Category", "Amount"), show="headings", style="mystyle.Treeview")
friend_expenses_tree.heading("Date", text="Date")                                                          
friend_expenses_tree.heading("Friend", text="Friend")
friend_expenses_tree.heading("Category", text="Category")
friend_expenses_tree.heading("Amount", text="Amount")
friend_expenses_tree.pack()
friend_expenses_tree.place(x=340, y=43, width=854, height=395)

friend_expenses_style = ttk.Style()
friend_expenses_style.theme_use("alt")
friend_expenses_style.configure("Friend_Treeview",
    background="#E0FFFF",  # Set background color to something distinct
    foreground="black",
    rowheight="25",
    fieldbackground="#E0FFFF"
)
friend_expenses_tree.tag_configure("lavender", background="#E6E6FA")

# Create and pack the "Friend" label and entry field
friend_label = tk.Label(friends_tab, text="Friend:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
friend_label.place(x=64.0, y=43.0)
friend_var = tk.StringVar()
friend_entry = tk.Entry(friends_tab, bd=1, highlightthickness=1, bg="#FFFFFF", fg="#000000", textvariable=friend_var)
friend_entry.place(x=64.0, y=73.0, width=212.0, height=30.0)

# Create and pack the "Category" label and entry field
category1_label = tk.Label(friends_tab, text="Category:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
category1_label.place(x=64.0, y=129.0)
categories = ["Return","Food", "Home", "Transport", "Shopping", "Others"]
category1_var = tk.StringVar()
category1_dropdown = ttk.Combobox(friends_tab, textvariable=category1_var, values=categories)
category1_dropdown.place(x=64.0, y=159.0, width=212.0, height=30.0)

# Create and pack the "Amount" label and entry field
amount1_label = tk.Label(friends_tab, text="Amount:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
amount1_label.place(x=64.0, y=215.0)
amount1_var = tk.DoubleVar()
amount1_entry = tk.Entry(friends_tab, bd=1, highlightthickness=1, bg="#FFFFFF", fg="#000000", textvariable=amount1_var)
amount1_entry.place(x=64.0, y=245.0, width=212.0, height=30.0)

# Create and pack the "Add Expense" button
add_friend_expense_button = tk.Button(
    friends_tab,
    text="Add Expense",
    command=add_friend_expense,
    font=("Inter ExtraBold", 16),
    bg="#E0D7FF",
    fg="#000000",
    bd=1, highlightthickness=1,
)
add_friend_expense_button.place(x=64.0, y=305.0, width=212, height=50)

# Create and pack widgets for currency conversion
amount2_label = tk.Label(currency_converter_tab, text="Amount:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
amount2_label.place(x=150, y=80)
amount2_entry = tk.Entry(currency_converter_tab, bd=1, highlightthickness=1, bg="#FFFFFF", fg="#000000")
amount2_entry.place(x=150, y= 120, width=260, height=35)

from_currency_label = tk.Label(currency_converter_tab, text="From Currency:", font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
from_currency_label.place(x= 150, y= 170)
from_currency_var = tk.StringVar()
from_currency_dropdown = ttk.Combobox(currency_converter_tab, textvariable=from_currency_var, values=currencies)
from_currency_dropdown.place(x=150, y=200, width=260, height=35)

to_currency_label = tk.Label(currency_converter_tab, text="To Currency:",font=("Inter ExtraBold", 16), bg="#E0D7FF", fg="#000000")
to_currency_label.place(x=150, y=260)
to_currency_var = tk.StringVar()
to_currency_dropdown = ttk.Combobox(currency_converter_tab, textvariable=to_currency_var, values=currencies)
to_currency_dropdown.place(x=150, y=290, width=260, height=35)

convert_button = tk.Button(currency_converter_tab, text="Convert", command=convert_currency, font=("Inter ExtraBold", 16), fg="#000000", bd=1, highlightthickness=1)
convert_button.place(x=150, y=360, width=260, height=50)

result_label= tk.Label(currency_converter_tab, font=("Inter ExtraBold", 18), bg="#FFFFFF", fg="#000000",  relief="raised")
result_label.place(x=150, y= 460, width=280, height=60)

image_path = "/Users/shravanicmali18/Downloads/Currency.jpeg"  # Change to your image file path
  # Change to your image file path
image = Image.open(image_path)
image = image.resize((600, 500))  # Adjust the size as needed
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(currency_converter_tab, image=photo, bg="white")
image_label.photo = photo
image_label.place(x=600, y=90) 




home_label= tk.Label(home_tab, text="Welcome!!",font=("Times", 50), bg="#FFFFFF", fg="#000000")
home1_label = tk.Label(home_tab, text="Manage your finances and start saving today", font=("Times", 25), bg="#FFFFFF",fg="#000000" )
description_label = tk.Label(home_tab, text="Track balances", font=("Times", 40), bg="lavenderBlush", fg="purple")
description_label1 = tk.Label(home_tab, text="Keep track of shared expenses, balances, and who owes who.", font=("Times", 25), bg="lavenderBlush", fg="purple")
description_label2 = tk.Label(home_tab, text="Graphical Representation", font=("Times", 40), bg="honeydew", fg="purple")
description_label21 = tk.Label(home_tab, text="Visualize Daily Expenses with Pie Charts and Line Graphs.", font=("Times", 25), bg="honeydew", fg="purple")
description_label3 = tk.Label(home_tab, text="Currency Conversion", font=("Times", 40), bg="light yellow", fg="purple")
description_label31 = tk.Label(home_tab, text="Seamless Currency Conversion for Effortless Global Travel.", font=("Times", 25), bg="light yellow", fg="purple")
description_label4 = tk.Label(home_tab, text="Pay friends back", font=("Times", 40), bg="PeachPuff", fg="purple")
description_label41 = tk.Label(home_tab, text="Effortlessly settle up with a friendby keeping \nrecords of transactions", font=("Times", 25), bg="PeachPuff", fg="purple")

home_label.place(x=60, y=60)
home1_label.place(x=70, y=130)
description_label.place(x=800, y=200)
description_label1.place(x=800, y=250)
description_label2.place(x=800,y=350)
description_label21.place(x=800,y=400)
description_label3.place(x=800,y=500)
description_label31.place(x=800,y=550)
description_label4.place(x=800,y=650)
description_label41.place(x=800,y=700)
# Load and display the image in the "Home" tab at a medium size
image_path = "/Users/shravanicmali18/Downloads/Finance.jpeg"  # Change to your image file path
  # Change to your image file path
image = Image.open(image_path)
image = image.resize((600, 500))  # Adjust the size as needed
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(home_tab, image=photo, bg="white")
image_label.photo = photo
image_label.place(x=60, y=200)  # Adjust the position as needed


friend_expenses_data = []
# List to store expenses data
expenses_data = []

update_pie_chart()
update_line_graph()

# Start the Tkinter main loop
window.mainloop()