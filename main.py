from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

GREEN = "#9bdeac"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generates a random strong password."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    pass_word = "".join(password_list)
    password_entry.insert(0, pass_word)
    pyperclip.copy(pass_word)


# ---------------------------- search for password ------------------------------- #

def search_for_website():
    """Search for the website's email and password in the json file"""
    searched_website = website_entry.get().lower()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if searched_website == "list":
            # Change the way data is formatted for the "list" option
            formatted_data = []
            for website, credentials in data.items():
                formatted_data.append(
                    f"Website: {website}\nEmail: {credentials['email']}\nPassword: {credentials['password']}\n")

            # Save the formatted data to a text file
            with open("data.txt", "w") as file:
                file.write("\n".join(formatted_data))

            messagebox.showinfo(title="Success", message="Your list is now ready in data.txt")
        elif searched_website in data:
            email = data[searched_website]["email"]
            password = data[searched_website]["password"]
            messagebox.showinfo(title=searched_website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for '{searched_website}' exists.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Saves the website/email/password entries into a file that will be a note saved on your pc."""
    website = website_entry.get().lower()
    email = email_entry.get().lower()
    password = password_entry.get().lower()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # updating old data with new data
            data.update(new_data)

            with open("data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=50)
window.minsize(width=500, height=400)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# ---------------------------- Labels ------------------------------- #
website_label = Label(text="Website:", font=("Arial", 10, "bold"))
website_label.grid(row=1, column=0)

username_label = Label(text="Email/Username", font=("Arial", 10, "bold"))
username_label.config(padx=5)
username_label.grid(row=2, column=0)

password_label = Label(text="Password:", font=("Arial", 10, "bold"))
password_label.grid(row=3, column=0)

# ---------------------------- Entries ------------------------------- #
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=56)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "sabbaghzaid88@gmail.com")

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

# ---------------------------- Buttons ------------------------------- #
generate_password_button = Button(text="Generate Password:", width=15, command=generate_password,
                                  font=("Arial", 10, "bold"))
generate_password_button.config(padx=5, pady=5)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=41, command=save, font=("Arial", 10, "bold"))
add_button.config(padx=5, pady=5)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=15, command=search_for_website, font=("Times New Roman", 10, "bold"))
search_button.config(padx=5, pady=5)
search_button.grid(row=1, column=2)

window.mainloop()
