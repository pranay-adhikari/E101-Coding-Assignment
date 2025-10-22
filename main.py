from library_books import library_books
from datetime import datetime, timedelta

# -------- Level 1 --------
# TODO: Create a function to view all books that are currently available
# Output should include book ID, title, and author

# Prints the title, ID, and author of all books available for checkout
def available_books():
    print("Available books: ")
    for book in library_books:
        if book["available"]: 
            print(f'Title: {book["title"]}, ID: {book["id"]}, Author: {book["author"]}')

# -------- Level 2 --------
# TODO: Create a function to search books by author OR genre
# Search should be case-insensitive
# Return a list of matching books

# Loops through the books returning a list of all books with author or genre matches. The search query is case-insensitive
def search_book():
    matching_books = []
    query = input("Search for a book by author or genre: ").strip().lower()
    for book in library_books:
        author = book["author"].lower()
        genre = book["genre"].lower()
        if query == author or query == genre:
            matching_books.append(book)
    return matching_books

# -------- Level 3 --------
# TODO: Create a function to checkout a book by ID
# If the book is available:
#   - Mark it unavailable
#   - Set the due_date to 2 weeks from today
#   - Increment the checkouts counter
# If it is not available:
#   - Print a message saying it's already checked out

# Attempts to checkout status of the book with the cooresponding ID parameter, printing a failure message otherwise or in the case of invalid ID
def checkout_book(ID):
    # Because we're accepting user input, we have to make sure the book actually exists
    book_to_checkout = None
    for book in library_books:
        if book["id"] == ID:
            book_to_checkout = book
            break
    if book_to_checkout == None:
        print(f"Book with ID {ID} does not exist")

    # If the book is available, we check it out. Otherwise, we print that it's already been checked out
    if book_to_checkout["available"]:
        due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")
        book_to_checkout["due_date"] = due_date
        book_to_checkout["available"] = False
        book_to_checkout["checkouts"] += 1
        print(book)
    else:
        print(f"{book_to_checkout} is already checked out")

# -------- Level 4 --------
# TODO: Create a function to return a book by ID
# Set its availability to True and clear the due_date

# TODO: Create a function to list all overdue books
# A book is overdue if its due_date is before today AND it is still checked out


# -------- Level 5 --------
# TODO: Convert your data into a Book class with methods like checkout() and return_book()
# TODO: Add a simple menu that allows the user to choose different options like view, search, checkout, return, etc.

# -------- Optional Advanced Features --------
# You can implement these to move into Tier 4:
# - Add a new book (via input) to the catalog
# - Sort and display the top 3 most checked-out books
# - Partial title/author search
# - Save/load catalog to file (CSV or JSON)
# - Anything else you want to build on top of the system!

if __name__ == "__main__":
    # You can use this space to test your functions
    checkout_book("B2")