import json
import random
from datetime import datetime


def timestamp():
    return datetime.now().strftime("%d-%m-%Y %H:%M")

class Book:

    def __init__(self, book_id, title, author, genre, year, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.copies = copies
        self.available = copies

    def display_info(self):

        print(f"Book ID: {self.book_id}")
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Genre: {self.genre}")
        print(f"Year: {self.year}")
        print(f"Copies: {self.copies}")
        print(f"Available: {self.available}")

    def to_dict(self):

        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "copies": self.copies,
            "available": self.available
        }

    def borrow(self):
        if self.available > 0:
            self.available -= 1
            return True
        else:
            return False

    def return_copy(self):

        if self.available == self.copies:
            return False
        else:
            self.available += 1
            return True

class Member:

    def __init__(self, member_id, username, pin):
        self.member_id = member_id
        self.username = username
        self.pin = pin
        self.borrowed_books = []
        self.records = []

    def to_dict(self):

        borrowed_book_ids = []

        for book in self.borrowed_books:
            borrowed_book_ids.append(book.book_id)
        return {
            "username": self.username,
            "pin": self.pin,
            "borrowed books": borrowed_book_ids,
            "records": self.records
        }
    def borrow_book(self, book):

        if book in self.borrowed_books:
            return False

        if book.borrow():
            self.borrowed_books.append(book)
            self.records.append(f"{timestamp()}\nBorrowed: {book.title}")
            return True
        else:
            return False

    def return_book(self, book):

        if book not in self.borrowed_books:
            return False

        if book.return_copy():
            self.borrowed_books.remove(book)
            self.records.append(f"{timestamp()}\nReturned: {book.title}")
            return True
        else:
            return False

    def view_borrowed_books(self):

        if not self.borrowed_books:
            print("No books borrowed at the moment.")
            return
        else:
            for book in self.borrowed_books:
                print(f"{book.book_id} - {book.title}")
                print()


    def view_records(self):
        if not self.records:
            print("No transaction made")

        else:
            for record in self.records:
                print(record)
                print()

class Admin:

    def __init__(self, username, pin):
        self.username = username
        self.pin = pin

    def to_dict(self):

        return{
            "pin": self.pin
        }

class Library:

    def __init__(self):
        self.books = {}
        self.members = {}
        self.admins = {}
        self.books_file_path = "Library_books_V2.json"
        self.members_file_path = "Library_members_V2.json"
        self.admins_file_path = "Library_admins_V2.json"


# PERSISTENT MEMORY


    def load_books(self):

        try:
            with open(self.books_file_path, "r") as file:
                raw_books = json.load(file)
        except FileNotFoundError:
            self.books = {}
            return
        except json.JSONDecodeError:
            self.books = {}
            return

        self.books = {}

        for book_id, information in raw_books.items():
            book = Book(
                        book_id,
                        information["title"],
                        information["author"],
                        information["genre"],
                        information["year"],
                        information["copies"]
                        )
            book.available = information["available"]
            self.books[book_id] = book

    def load_members(self):
        try:
            with open(self.members_file_path, "r") as file:
                raw_members = json.load(file)
        except FileNotFoundError:
            self.members = {}
            return
        except json.JSONDecodeError:
            self.members = {}
            return

        self.members = {}

        for member_id, information in raw_members.items():
            member = Member(
                member_id,
                information["username"],
                information["pin"]
            )
            member.records = information["records"]

            for book_id in information["borrowed books"]:
                member.borrowed_books.append(self.books[book_id])

            self.members[member_id] = member

    def load_admins(self):
        try:
            with open(self.admins_file_path, "r") as file:
                raw_admins = json.load(file)
        except FileNotFoundError:
            self.admins = {}
            return
        except json.JSONDecodeError:
            self.admins = {}
            return

        self.admins = {}

        for username, information in raw_admins.items():
            admin = Admin(
                username,
                information["pin"]
            )
            self.admins[username] = admin

    def load_data(self):
        self.load_books()
        self.load_members()
        self.load_admins()

    def save_books(self):

        json_books = {}

        for book_id, book in self.books.items():
            json_books[book_id] = book.to_dict()

        with open(self.books_file_path, "w") as file:
            json.dump(json_books, file, indent = 4)

    def save_members(self):

        json_members = {}

        for member_id, member in self.members.items():
            json_members[member_id] = member.to_dict()

        with open(self.members_file_path, "w") as file:
            json.dump(json_members, file, indent = 4)

    def save_admins(self):

        json_admins = {}

        for username, admin in self.admins.items():
            json_admins[username] = admin.to_dict()

        with open(self.admins_file_path, "w") as file:
            json.dump(json_admins, file, indent = 4)

    def save_data(self):
        self.save_books()
        self.save_members()
        self.save_admins()
        

# HELPER FUNCTIONS


    def generate_book_id(self):
        num = 1
        while True:
            book_id = f"B{num:04}"
            if book_id not in self.books:
                return book_id
            num += 1

    def generate_member_id(self):

        while True:
            num = random.randint(1, 9999999)
            member_id = f"M{num:07}"
            if member_id not in self.members:
                return member_id

    def find_book(self, book_id):
        return self.books.get(book_id)


    def find_member(self, member_id):
        return self.members.get(member_id)

    def find_username(self, username):
        for member in self.members.values():
            if member.username == username:
                return member
        return None

    def find_book_title(self, title):
        for book in self.books.values():
            if title.lower() in book.title.lower():
                return book
        return None

    def find_admin(self, username):
        return self.admins.get(username)

    def get_pin(self):
        user_input = input("PIN: ")
        if len(user_input) != 4 or not user_input.isdigit():
            return None
        return int(user_input)

    def search_book(self):
        title = input("Title: ")
        book = self.find_book_title(title)
        if book:
            book.display_info()
        else:
            print("Book not found.")


# ADMIN TASKS


    def add_book(self, title, author, genre, year, copies):
        book_id = self. generate_book_id()
        book = Book(
            book_id,
            title,
            author,
            genre,
            year,
            copies
        )
        if self.find_book_title(title):
            return None

        self.books[book_id] = book
        self.save_books()
        return book

    def add_member(self, username, pin):

        if self.find_username(username):
            return None

        member_id = self.generate_member_id()
        member = Member(
            member_id,
            username,
            pin
        )
        self.members[member_id] = member
        self.save_members()
        return member
    def borrow_book(self, member_id, title):

        member = self.find_member(member_id)
        book = self.find_book_title(title)
        if not book or not member:
            return False
        if member.borrow_book(book):
            self.save_books()
            self.save_members()
            return True
        return False

    def return_book(self, member_id, title):

        member = self.find_member(member_id)
        book = self.find_book_title(title)

        if not book or not member:
            return False
        if member.return_book(book):
            self.save_books()
            self.save_members()
            return True
        return False

    def remove_book(self, book_id):

        book = self.find_book(book_id)
        if not book:
            return False

        if book.available != book.copies:
            return False

        del self.books[book_id]
        self.save_books()
        return True

    def remove_member(self, member_id):

        member = self.find_member(member_id)
        if not member:
            return False

        if member.borrowed_books:
            return False

        del self.members[member_id]
        self.save_members()
        return True


# LOGIN OPERATIONS


    def login_member(self, username, pin):
        member = self.find_username(username)

        if not member:
            return None

        if member.pin == pin:
            return member
        return None

    def login_admin(self, username, pin):
        admin = self.find_admin(username)

        if not admin:
            return None

        if admin.pin == pin:
            return admin
        return None


# MENU


    def main_menu(self):
        while True:
            print("============== LIBRARY ==============")
            print("1. Member Sign Up")
            print("2. Member Login")
            print("3. Admin Login")
            print("0. Exit")

            user_input = input("Choose an option above: ")
            try:
                option = int(user_input)
            except ValueError:
                print("Invalid option")
                continue
            if option == 0:
                print("Thanks for using our service!")
                break
            elif option == 1:
                username = input("Create a username: ")
                pin = self.get_pin()
                if pin is None:
                    print("PIN must be exactly four digits")
                    continue

                member = self.add_member(username, pin)
                if member:
                    print("Singed up successfully!")
                    print(f"Member ID: {member.member_id}")
                    self.member_menu(member)
                    print()
                else:
                    print("That username already exists.")
                    continue

            elif option == 2:
                username = input("Username: ")
                pin = self.get_pin()
                if pin is None:
                    print("PIN must be exactly four digits")
                    continue

                member = self.login_member(username, pin)
                if member:
                    print("Logged in successfully!")
                    print()
                    self.member_menu(member)
                else:
                    print("Invalid username or PIN")
                    continue

            elif option == 3:
                username = input("Username: ")
                pin = self.get_pin()
                if pin is None:
                    print("PIN must be exactly four digits")
                    continue

                admin = self.login_admin(username, pin)

                if admin:
                    print("Logged in successfully!")
                    print()
                    self.admin_menu()
                else:
                    print("Invalid username or PIN")
                    continue
            else:
                print("Invalid option")

    def member_menu(self, member):

        while True:
            print("============== MEMBER MENU ==============")
            print("1. Borrow Book")
            print("2. Return Book")
            print("3. Search Book")
            print("4. View Borrowed Books")
            print("5. View Transaction History")
            print("0. Exit")
            user_input = input("Choose an option above: ")
            try:
                option = int(user_input)
            except ValueError:
                print("Invalid option")
                continue
            if option == 0:
                break

            elif option == 1:
                title = input("Title: ")
                if self.borrow_book(member.member_id, title):
                    print("Book borrowed successfully!")
                else:
                    print("Unable to borrow book")

            elif option == 2:
                title = input("Title: ")
                if self.return_book(member.member_id, title):
                    print("Book returned successfully!")
                else:
                    print("Unable to return book")

            elif option == 3:
                self.search_book()

            elif option == 4:
                member.view_borrowed_books()

            elif option == 5:
                member.view_records()

            else:
                print("Invalid option")

    def admin_menu(self):
        while True:
            print("============== ADMIN MENU ==============")
            print("1. Add Book")
            print("2. Remove Book")
            print("3. View Books")
            print("4. Search Book")
            print("5. Add Member")
            print("6. Remove Member")
            print("7. View Members")
            print("0. Logout")

            user_input = input("Choose an option above: ")
            try:
                option = int(user_input)
            except ValueError:
                print("Invalid option")
                continue

            if option == 0:
                break

            elif option == 1:
                title = input("Title: ")
                author = input("Author: ")
                genre = input("Genre: ")
                user_input1 = input("Year: ")
                try:
                    year = int(user_input1)
                except ValueError:
                    print("Invalid year.")
                    continue
                if year < 0:
                    print("Invalid year.")
                    continue

                user_input2 = input("Copies: ")
                try:
                    copies = int(user_input2)
                except ValueError:
                    print("Invalid number.")
                    continue
                if copies < 0:
                    print("Invalid number.")
                    continue

                book = self.add_book(title, author, genre, year, copies)

                if book:
                    print("Book added successfully!")
                else:
                    print("That book already exists.")

            elif option == 2:
                book_id = input("Enter book ID: ")
                if self.remove_book(book_id):
                    print("Book removed successfully!")
                else:
                    print("Unable to remove book.")
                    print("Please check the book ID.")

            elif option == 3:
                if not self.books:
                    print("No books available at the moment.")
                else:
                    for book in self.books.values():
                        print(f"{book.book_id} - {book.title}")

            elif option == 4:
                self.search_book()

            elif option == 5:
                username = input("Username: ")
                user_input = input("PIN:")
                if len(user_input) != 4 or not user_input.isdigit():
                    print("PIN must be exactly four digits")
                    continue
                pin = int(user_input)
                member = self.add_member(username, pin)
                if member:
                    print(f"Member ID: {member.member_id}")
                else:
                    print("That username already exists.")

            elif option == 6:
                member_id = input("Enter member ID: ")

                if self.remove_member(member_id):
                    print("Member removed successfully!")
                else:
                    print("Unable to remove member.")

            elif option == 7:
                if not self.members:
                    print("No members at the moment.")
                else:
                    for member in self.members.values():
                        print(f"{member.member_id} - {member.username}")

            else:
                print("Invalid option")


# MAIN


library = Library()
library.load_data()
library.main_menu()