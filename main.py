from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT = "Cousine NF"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_random = [random.choice(letters) for _ in range(random.randint(8, 10))]
    symbols_random = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    numbers_random = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    # concatenate 3 list to one
    pass_list = letters_random + symbols_random + numbers_random
    random.shuffle(pass_list)
    pass_list = "".join(pass_list)
    if password_entry.get():
        password_entry.delete(0, END)
        password_entry.insert(0, pass_list)
    else:
        password_entry.insert(0, pass_list)
    pyperclip.copy(pass_list)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    email = email_username_entry.get()
    password = password_entry.get()
    website = website_entry.get().title()
    new_data = {website: {"email": email,
                          "password": password}
                }

    if not email or not website:
        messagebox.showwarning(title="Error", message="Please fill out all required fields.")
        return
    else:
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)
                # Updating data
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                # Writing new_data to file and creating one if it doesn't exist
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            password_entry.delete(0, END)
            website_entry.delete(0, END)


# ------------------------- SEARCH PASSWORD --------------------------- #
def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            try:
                messagebox.showinfo(title=f"{website}", message=f"Email: {data[website]['email']}\n"
                                                                f"Password: {data[website]['password']}")
            except KeyError as error_key:
                messagebox.showwarning(title="Not Found", message=f"No details for {error_key} exists")
    except FileNotFoundError:
        messagebox.showwarning(title=f"No Data File", message=f"No Data File Was Found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=1)

# Labels
website_label = Label(text="Website", highlightthickness=0, font=(FONT, 10, "normal"))
website_label.grid(column=0, row=2)

email_username = Label(text="Email/Username", highlightthickness=0, font=(FONT, 10, "normal"))
email_username.grid(column=0, row=3)

password_label = Label(text="Password", highlightthickness=0, font=(FONT, 10, "normal"))
password_label.grid(column=0, row=4)

# Buttons
password_button = Button(text="Generate Password", font=(FONT, 10, "normal"), command=generate_password)
password_button.grid(column=2, row=4)

add_button = Button(text="Add", width=45, font=(FONT, 10, "normal"), command=save)
add_button.grid(column=1, row=5, columnspan=2)

search_button = Button(text="Search", width=17, font=(FONT, 10, "normal"), command=find_password)
search_button.grid(column=2, row=2)

# Entries
website_entry = Entry(width=23)
website_entry.grid(column=1, row=2)
website_entry.focus()

email_username_entry = Entry(width=45)
email_username_entry.grid(column=1, row=3, columnspan=2)
email_username_entry.insert(0, "user@email.com")

password_entry = Entry(width=23)
password_entry.grid(column=1, row=4)

window.mainloop()
