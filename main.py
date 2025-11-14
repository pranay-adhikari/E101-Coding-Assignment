"""
Python documentation references:

- datetime module: https://docs.python.org/3/library/datetime.html
- timedelta class: https://docs.python.org/3/library/datetime.html#timedelta-objects
- json module: https://docs.python.org/3/library/json.html
- csv module: https://docs.python.org/3/library/csv.html
- list comprehensions: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
- @staticmethod signature: https://docs.python.org/3/library/functions.html#staticmethod
- lambda functions: https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
- exception handling: https://docs.python.org/3/tutorial/errors.html#handling-exceptions

I used AI (claude.ai) to help me figure out the syntax for parsing a string time into a datetime object
"""

from library_books import library_books
from datetime import datetime, timedelta
import json
import csv

# Menu will loop until user exits
menu_loop = True

# Book class that can be used to create book objects
class Book:
    # Static variable library to store book objects
    library = []

    # Create and store book objects in library
    def __init__(self, id, title, author, genre, available, due_date, checkouts):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available
        self.due_date = due_date
        self.checkouts = checkouts
        Book.library.append(self)

    # -------- Level 1 --------
    # TODO: Create a function to view all books that are currently available
    # Output should include book id, title, and author

    # Prints the title, id, and author of all books available for checkout
    @staticmethod
    def available_books():
        available_books = [book for book in Book.library if book.available]
        if not available_books:
            print("There are currently no available books")
        else:
            print("Available books:")
            for book in available_books:
                print(f'ID: {book.id}, Title: {book.title}, Author: {book.author}')

    # -------- Level 2 --------
    # TODO: Create a function to search books by author OR genre
    # Search should be case-insensitive
    # Return a list of matching books

    # Loops through the books returning a list of all books with author or genre matches. The search query is case-insensitive, and allows partial inputs
    @staticmethod
    def search_for_book():
        matching_books = []
        query = input("Search for a book by author or genre: ").strip().lower()
        for book in Book.library:
            author = book.author.lower()
            genre = book.genre.lower()
            if query in author or query in genre:
                matching_books.append(book)
        return matching_books

    # -------- Level 3 --------
    # TODO: Create a function to checkout a book by id
    # If the book is available:
    #   - Mark it unavailable
    #   - Set the due_date to 2 weeks from today
    #   - Increment the checkouts counter
    # If it is not available:
    #   - Print a message saying it's already checked out

    # Attempts to checkout status of the book with the cooresponding id parameter, printing a failure message otherwise or in the case of invalid id
    @staticmethod
    def checkout_book(id):
        # Because we're accepting user input, we have to make sure the book actually exists
        book = Book.get_book(id)
        if book is None:
            print(f"There is no book with id: {id}")
            return -1

        # If the book is available, we check it out. Otherwise, we print that it's already been checked out
        if book.available:
            due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")
            book.due_date = due_date
            book.available = False
            book.checkouts += 1
            print(f"You've checked out \"{book.title}\". Its due date is {book.due_date}.")
        else:
            print(f"\"{book.title}\" is already checked out")

    # -------- Level 4 --------
    # TODO: Create a function to return a book by id
    # Set its availability to True and clear the due_date
    @staticmethod
    def return_book(id):
        book = Book.get_book(id)
        if book is None:
            print(f"There is no book with id: {id}")
            return -1
        if book.available:
            print(f"\"{book.title}\" is not checked out.")
        else:
            book.available = True
            book.due_date = None
            print(f"\"{book.title}\" successfully returned.")

    # TODO: Create a function to list all overdue books
    # A book is overdue if its due_date is before today AND it is still checked out
    @staticmethod
    def list_overdue_books():
        today = datetime.today().date()
        overdue_books = []
        for book in Book.library:
            if not book.available and book.due_date is not None:
                due_date = datetime.strptime(book.due_date, "%Y-%m-%d").date()
                if due_date < today:
                    overdue_books.append(book)
        if not overdue_books:
            print("No overdue books")
        else:
            for book in overdue_books:
                print(f'Overdue: {book.title} by {book.author}, Due: {book.due_date}')
        

    # Prints 3 most checked out books
    @staticmethod
    def most_checked_out():
        # We can use a lambda expression here instead of creating a new function to pass in for the key
        by_checkouts = sorted(Book.library, key=lambda b: b.checkouts, reverse=True)
        if not by_checkouts:
            print("There are no books in the library")
        else:
            for book in by_checkouts[:3]:
                print(book)
    
    # Export catalog to .json or .csv
    @staticmethod
    def export():
        choice = input("Export to JSON or CSV?\n1: JSON\n2: CSV\n\n").strip()
        if choice == "1":
            Book.export_to_json()
        elif choice == "2":
            Book.export_to_csv()
        else:
            print("Not a valid choice")

    # -------- Helper Functions --------
    # If a book with the id {id} exists, we return the book. Otherwise, false
    @staticmethod
    def get_book(id):
        for book in Book.library:
            if book.id == id:
                return book
        return None
    
    @staticmethod
    def library_to_dictionaries():
        library_list = []
        for book in Book.library:
            book_dict = {"id":book.id, "title":book.title, "author":book.author, "genre":book.genre, "available":book.available, "due_date":book.due_date, "checkouts":book.checkouts}
            library_list.append(book_dict)
        return library_list
    
    # Returns whether or not {id} is unique
    @staticmethod
    def unique_id(id):
        for book in Book.library:
            if book.id == id:
                return False
        return True
    
    # Exports catalog to json file
    @staticmethod
    def export_to_json():
        books_data = Book.library_to_dictionaries()
        filename = "library_books.json"
        with open(filename, 'w') as json_file:
            json.dump(books_data, json_file, indent=4)
        print(f"Successfully exported catalog to {filename}")
    
    # Exports catalog to csv file
    @staticmethod
    def export_to_csv():
        # Writing straight to csv will remove 'None' values, so we must convert them to strings
        books_data = Book.library_to_dictionaries()
        for book in books_data:
            if book["due_date"] is None:
                book["due_date"] = "None"

        filename = "library_books.csv"
        field_names = ["id", "title", "author", "genre", "available", "due_date", "checkouts"]
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(books_data)
        print(f"Successfully exported catalog to {filename}")

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Genre: {self.genre}, Available: {self.available}, Checkouts: {self.checkouts}"

# -------- Level 5 --------
# TODO: Convert your data into a Book class with methods like checkout() and return_book()
# TODO: Add a simple menu that allows the user to choose different options like view, search, checkout, return, etc.
def menu():
    global menu_loop
    print('-------------------------------')
    choice = input("What would you like to do? Enter your choice:\n1: View available books\n2: Search for a book\n3: Checkout a book\n4: Return a book\n5: View most checked out books\n6: List overdue books\n7: Add a book\n8: Remove a book\n9: Export catalog to file\n0: Exit\n\n").strip()
    print()
    match choice:
        case "1":
            Book.available_books()
        case "2":
            # Because the instructions explicitly say to return the list of books and not just print them, I return them and then print them afterwards
            search_results = Book.search_for_book()
            for book in search_results:
                print(book)
            if not search_results:
                print("No books match your search")
        case "3":
            id = input("ID of the book to checkout: ").strip()
            Book.checkout_book(id)
        case "4":
            id = input("ID of the book to return: ").strip()
            Book.return_book(id)
        case "5":
            Book.most_checked_out()
        case "6":
            Book.list_overdue_books()
        case "7":
            add_book()
        case "8":
            delete_book()
        case "9":
            Book.export()
        case "0":
            menu_loop = False
            print("Goodbye!")
        
        # For handling default case
        case _:
            print("Not a valid option")

def populate_library():
    for book in library_books:
        Book(book["id"], book["title"], book["author"], book["genre"], book["available"], book["due_date"], book["checkouts"])

# When adding a book for the first time, it should be available and have no due date/checkouts as well as a unique id
def add_book():
    id = input("ID: ").strip()
    if not Book.unique_id(id):
        print("Not a unique id")
        return -1
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    genre = input("Genre: ").strip()
    Book(id=id, title=title, author=author, genre=genre, available=True, due_date=None, checkouts=0)

# Deletes a book from the catalog
def delete_book():
    id = input("ID: ").strip()
    book = Book.get_book(id)
    if book is None:
        print("Invalid ID")
    else:
        Book.library.remove(book)
        print(f'\'{book.title}\' has been removed from the catalog')

# -------- Optional Advanced Features --------
# You can implement these to move into Tier 4:
# - Add a new book (via input) to the catalog
# - Sort and display the top 3 most checked-out books
# - Partial title/author search
# - Save/load catalog to file (CSV or JSON)
# - Anything else you want to build on top of the system!

if __name__ == "__main__":
    try:
        populate_library()
        while menu_loop:
            menu()
            print()
    except KeyboardInterrupt:
        print("Goodbye!")