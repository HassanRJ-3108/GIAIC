# Personal Library Manager
# This program helps you manage your book collection

# Import the json module to save and load data
import json
import os

# List to store all books
books = []

# File to save the library data
file_name = "library.txt"

# Function to display the main menu
def show_menu():
    """Shows the main menu options to the user"""
    print("\n===== Personal Library Manager =====")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")
    
    # Get user's choice
    choice = input("Enter your choice (1-6): ")
    return choice

# Function to add a new book
def add_book():
    """Asks user for book details and adds it to the library"""
    print("\n----- Add a Book -----")
    
    # Get book details from user
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    
    # Make sure year is a valid number
    year = 0
    while year == 0:
        try:
            year = int(input("Enter the publication year: "))
        except:
            print("Please enter a valid year (number only)")
    
    genre = input("Enter the genre: ")
    
    # Check if book is read
    read_answer = input("Have you read this book? (yes/no): ")
    # Convert yes/no to True/False
    is_read = read_answer.lower() in ["yes", "y"]
    
    # Create a dictionary to store book info
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": is_read
    }
    
    # Add the book to our list
    books.append(book)
    print("Book added successfully!")

# Function to remove a book
def remove_book():
    """Removes a book from the library by title"""
    print("\n----- Remove a Book -----")
    
    # Get the title to remove
    title = input("Enter the title of the book to remove: ")
    
    # Keep track if we found the book
    found = False
    
    # Loop through books to find the one to remove
    for i in range(len(books)):
        # Check if this is the book we want to remove
        if books[i]["title"].lower() == title.lower():
            # Remove the book
            del books[i]
            print("Book removed successfully!")
            found = True
            break
    
    # If we didn't find the book
    if not found:
        print("Book not found. Nothing removed.")

# Function to search for books
def search_book():
    """Searches for books by title or author"""
    print("\n----- Search for a Book -----")
    print("Search by:")
    print("1. Title")
    print("2. Author")
    
    # Get search type
    search_choice = input("Enter your choice (1-2): ")
    
    # List to store matching books
    found_books = []
    
    # Search by title
    if search_choice == "1":
        title = input("Enter the title: ")
        
        # Look through all books
        for book in books:
            # Check if title matches (ignore case)
            if title.lower() in book["title"].lower():
                found_books.append(book)
        
        search_type = "title"
        search_term = title
    
    # Search by author
    elif search_choice == "2":
        author = input("Enter the author: ")
        
        # Look through all books
        for book in books:
            # Check if author matches (ignore case)
            if author.lower() in book["author"].lower():
                found_books.append(book)
        
        search_type = "author"
        search_term = author
    
    # Invalid choice
    else:
        print("Invalid choice.")
        return
    
    # Display results
    if found_books:
        print(f"\nMatching Books for {search_type} '{search_term}':")
        for i, book in enumerate(found_books):
            # Show book details
            read_status = "Read" if book["read"] else "Unread"
            print(f"{i+1}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        print(f"No books found matching {search_type} '{search_term}'.")

# Function to display all books
def display_books():
    """Shows all books in the library"""
    print("\n----- Your Library -----")
    
    # Check if library is empty
    if not books:
        print("Your library is empty.")
        return
    
    # Display each book
    for i, book in enumerate(books):
        # Show book details
        read_status = "Read" if book["read"] else "Unread"
        print(f"{i+1}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

# Function to display statistics
def display_stats():
    """Shows statistics about the library"""
    print("\n----- Library Statistics -----")
    
    # Total number of books
    total_books = len(books)
    print(f"Total books: {total_books}")
    
    # If there are no books, stop here
    if total_books == 0:
        return
    
    # Count read books
    read_books = 0
    for book in books:
        if book["read"]:
            read_books += 1
    
    # Calculate percentage
    percentage = (read_books / total_books) * 100
    
    # Display statistics
    print(f"Books read: {read_books}")
    print(f"Books unread: {total_books - read_books}")
    print(f"Percentage read: {percentage:.1f}%")

# Function to save library to file
def save_library():
    """Saves the library to a file"""
    # Open file for writing
    with open(file_name, "w") as file:
        # Convert books list to JSON and save
        json.dump(books, file)

# Function to load library from file
def load_library():
    """Loads the library from a file"""
    global books
    
    # Check if file exists
    if os.path.exists(file_name):
        try:
            # Open file for reading
            with open(file_name, "r") as file:
                # Load books from JSON
                books = json.load(file)
            print(f"Loaded {len(books)} books from {file_name}")
        except:
            # If there's an error, start with empty library
            books = []
            print("Could not load library file. Starting with empty library.")
    else:
        print("No library file found. Starting with empty library.")

# Main function
def main():
    """Main function that runs the program"""
    # Load library when program starts
    load_library()
    
    # Keep running until user exits
    while True:
        # Show menu and get choice
        choice = show_menu()
        
        # Process user choice
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_stats()
        elif choice == "6":
            # Save library before exiting
            save_library()
            print("\nLibrary saved to file. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()

