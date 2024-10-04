from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8,10))]
    password_symbols = [choice(symbols) for _ in range(randint(2,4))]
    password_numbers = [choice(numbers) for _ in range(randint(2,4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    rg_password = "".join(password_list)
    password_entry.insert(0, f"{rg_password}")
    pyperclip.copy(rg_password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email_user = eu_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email_user,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="hold up, wait a minute, something aint right",
                            message="you forgot to fill out a field")
    else:
        try:
            with open("data.json", "r") as passwords_file:
                ## reading old data
                password_data = json.load(passwords_file)
        except FileNotFoundError:
            with open("data.json", "w") as passwords_file:
                ## saving updated data
                json.dump(new_data, passwords_file, indent=4)
        else:
            ## updating old data w/ new data
            password_data.update(new_data)
            with open("data.json", "w") as passwords_file:
                json.dump(password_data, passwords_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as passwords_file:
            password_data = json.load(passwords_file)
    except FileNotFoundError: ## use except method in rare occasions
        messagebox.showerror(title="hold up, wait a minute, something aint right", message="No Data File Found")
    else: ## use if/else methods for frequent errors
        if website in password_data:
            messagebox.showinfo(title="Data Retrieved", message=f"Data for: {website}"
                                                                f"\nEmail: {password_data[website]['email']}"
                                                                f"\nPassword: {password_data[website]['password']}")
        else:
            messagebox.showerror(title="hold up, wait a minute, something aint right",
                                 message="No details for the website exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("password manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
label_1 = Label(text="Website:")
label_1.grid(column=0, row=1)

label_2 = Label(text="Email/Username:")
label_2.grid(column=0,row=2)

label_3 = Label(text="Password:")
label_3.grid(column=0, row=3)

# entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

eu_entry = Entry(width=38)
eu_entry.grid(column=1, row=2, columnspan=2)
eu_entry.insert(0, "tyler02huy@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# buttons
rg_password_button = Button(text="Generate Password", command=generate_password)
rg_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
