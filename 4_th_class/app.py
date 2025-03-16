# Personal Library Manager - Streamlit Version
# This is a web interface for the library manager

# Import required libraries
import streamlit as st
import json
import os

# File to save the library data
FILE_NAME = "library.txt"

# Function to load library from file
def load_library():
    """Loads the library from a file and returns the books list"""
    # Check if file exists
    if os.path.exists(FILE_NAME):
        try:
            # Open file for reading
            with open(FILE_NAME, "r") as file:
                # Load books from JSON
                return json.load(file)
        except:
            # If there's an error, return empty list
            return []
    else:
        # If file doesn't exist, return empty list
        return []

# Function to save library to file
def save_library(books):
    """Saves the books list to a file"""
    # Open file for writing
    with open(FILE_NAME, "w") as file:
        # Convert books list to JSON and save
        
        json.dump(books, file)

# Main function
def main():
    # Set page title
    st.set_page_config(page_title="Personal Library Manager", page_icon="📚")
    
    # Display header
    st.title("📚 Personal Library Manager")
    
    # Initialize session state for books if not exists
    if 'books' not in st.session_state:
        st.session_state.books = load_library()
    
    # Create sidebar menu
    st.sidebar.title("Menu")
    page = st.sidebar.radio(
        "Choose an option:",
        ["View Books", "Add Book", "Remove Book", "Search Books", "Statistics"]
    )
    
    # Show different pages based on selection
    if page == "View Books":
        view_books()
    elif page == "Add Book":
        add_book()
    elif page == "Remove Book":
        remove_book()
    elif page == "Search Books":
        search_books()
    elif page == "Statistics":
        show_statistics()
    
    # Save books whenever the app runs
    save_library(st.session_state.books)

# Function to display all books
def view_books():
    """Shows all books in the library"""
    st.header("Your Library")
    
    # Check if library is empty
    if not st.session_state.books:
        st.info("Your library is empty. Add some books to get started!")
        return
    
    # Display each book in a nice format
    for i, book in enumerate(st.session_state.books):
        # Create a card-like display for each book
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            # Book details in first column
            with col1:
                # Show if book is read with an emoji
                read_status = "✅ Read" if book["read"] else "📖 Unread"
                
                # Display book information
                st.subheader(f"{i+1}. {book['title']}")
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Year:** {book['year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Status:** {read_status}")
            
            # Add a separator between books
            st.divider()

# Function to add a new book
def add_book():
    """Form to add a new book"""
    st.header("Add a New Book")
    
    # Create a form for adding books
    with st.form("add_book_form"):
        # Get book details
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=2100, value=2023)
        genre = st.text_input("Genre")
        read_status = st.checkbox("I have read this book")
        
        # Submit button
        submitted = st.form_submit_button("Add Book")
        
        # Process form submission
        if submitted:
            # Check if title and author are provided
            if title and author:
                # Create new book dictionary
                new_book = {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": read_status
                }
                
                # Add to books list
                st.session_state.books.append(new_book)
                st.success(f"'{title}' by {author} added successfully!")
            else:
                st.error("Please enter both title and author.")

# Function to remove a book
def remove_book():
    """Form to remove a book"""
    st.header("Remove a Book")
    
    # Check if library is empty
    if not st.session_state.books:
        st.info("Your library is empty. There are no books to remove.")
        return
    
    # Get list of book titles
    book_titles = [book["title"] for book in st.session_state.books]
    
    # Dropdown to select book to remove
    selected_title = st.selectbox("Select a book to remove:", book_titles)
    
    # Remove button
    if st.button("Remove Book"):
        # Find and remove the selected book
        for i, book in enumerate(st.session_state.books):
            if book["title"] == selected_title:
                # Remove the book
                del st.session_state.books[i]
                st.success(f"'{selected_title}' removed successfully!")
                break

# Function to search for books
def search_books():
    """Search for books by title or author"""
    st.header("Search Books")
    
    # Choose search type
    search_type = st.radio("Search by:", ["Title", "Author"])
    
    # Get search term
    search_term = st.text_input("Enter search term:")
    
    # Only search if a term is entered
    if search_term:
        # List to store results
        results = []
        
        # Search through books
        for book in st.session_state.books:
            # Search by title
            if search_type == "Title" and search_term.lower() in book["title"].lower():
                results.append(book)
            # Search by author
            elif search_type == "Author" and search_term.lower() in book["author"].lower():
                results.append(book)
        
        # Display results
        if results:
            st.subheader(f"Found {len(results)} books:")
            
            # Show each result
            for i, book in enumerate(results):
                # Create a nice display for each book
                with st.container():
                    # Show if book is read with an emoji
                    read_status = "✅ Read" if book["read"] else "📖 Unread"
                    
                    # Display book information
                    st.write(f"**{i+1}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
                
                # Add a separator between books
                st.divider()
        else:
            st.info(f"No books found matching {search_type.lower()} '{search_term}'.")

# Function to show statistics
def show_statistics():
    """Shows statistics about the library"""
    st.header("Library Statistics")
    
    # Get total number of books
    total_books = len(st.session_state.books)
    
    # Display total books
    st.subheader(f"Total Books: {total_books}")
    
    # If there are no books, stop here
    if total_books == 0:
        st.info("Add some books to see more statistics.")
        return
    
    # Count read books
    read_books = sum(1 for book in st.session_state.books if book["read"])
    unread_books = total_books - read_books
    
    # Calculate percentage
    percentage = (read_books / total_books) * 100
    
    # Display statistics in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Books Read", read_books)
    
    with col2:
        st.metric("Books Unread", unread_books)
    
    # Show reading progress
    st.subheader("Reading Progress")
    st.progress(percentage / 100)
    st.write(f"You've read {percentage:.1f}% of your library")
    
    # Create a simple chart
    st.subheader("Read vs Unread")
    st.bar_chart({"Read": read_books, "Unread": unread_books})

# Run the app
if __name__ == "__main__":
    main()

