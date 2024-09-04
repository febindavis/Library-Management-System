import mysql.connector
from mysql.connector import Error

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'library_db'
}

def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def add_book(connection):
    title = input("Enter book title: ")
    author = input("Enter author: ")
    quantity = int(input("Enter quantity: "))
    
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, author, quantity, available) VALUES (%s, %s, %s, %s)", 
                   (title, author, quantity, quantity))
    connection.commit()
    print("Book added successfully.")
    
def update_book(connection):
    book_id = int(input("Enter book ID to update: "))
    new_title = input("Enter new book title (leave blank to keep current): ")
    new_author = input("Enter new author (leave blank to keep current): ")
    new_quantity = input("Enter new quantity (leave blank to keep current): ")
    
    cursor = connection.cursor()
    
    update_query = "UPDATE books SET "
    update_values = []
    
    if new_title:
        update_query += "title = %s, "
        update_values.append(new_title)
    if new_author:
        update_query += "author = %s, "
        update_values.append(new_author)
    if new_quantity:
        update_query += "quantity = %s, available = %s "
        update_values.append(int(new_quantity))
        update_values.append(int(new_quantity))
    else:
        update_query = update_query.rstrip(', ')
    
    update_query += "WHERE id = %s"
    update_values.append(book_id)
    
    cursor.execute(update_query, tuple(update_values))
    connection.commit()
    print("Book updated successfully.")
    
def rent_book(connection):
    book_id = int(input("Enter book ID to rent out: "))
    
    cursor = connection.cursor()
    cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        cursor.execute("UPDATE books SET available = available - 1 WHERE id = %s", (book_id,))
        cursor.execute("INSERT INTO transactions (book_id, action) VALUES (%s, 'rented out')", (book_id,))
        connection.commit()
        print("Book rented out successfully.")
    else:
        print("No copies available to rent out.")
        
def view_all_books(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    
    if rows:
        print("\nAll Books:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}, Available: {row[4]}")
    else:
        print("No books found.")
        
def view_transactions(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    
    if rows:
        print("\nAll Transactions:")
        for row in rows:
            print(f"ID: {row[0]}, Book ID: {row[1]}, Action: {row[2]}, Date: {row[3]}")
    else:
        print("No transactions found.")
        
def delete_book(connection):
    book_id = int(input("Enter book ID to delete: "))
    
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    connection.commit()
    print("Book deleted successfully.")
    
def search_books(connection):
    search_term = input("Enter title or author to search: ")
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", 
                   ('%' + search_term + '%', '%' + search_term + '%'))
    rows = cursor.fetchall()
    
    if rows:
        print("\nSearch Results:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}, Available: {row[4]}")
    else:
        print("No books found matching the search criteria.")

def main():
    connection = connect_to_db()
    if not connection:
        return
    
    while True:
        print("\nLibrary Management System")
        print("1. Add New Book")
        print("2. Update Book")
        print("3. Rent Out Book")
        print("4. View All Books")
        print("5. View Transactions")
        print("6. Delete Book")
        print("7. Search for a Book")
        print("8. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_book(connection)
        elif choice == '2':
            update_book(connection)
        elif choice == '3':
            rent_book(connection)
        elif choice == '4':
            view_all_books(connection)
        elif choice == '5':
            view_transactions(connection)
        elif choice == '6':
            delete_book(connection)
        elif choice == '7':
            search_books(connection)
        elif choice == '8':
            print("Exiting...")
            connection.close()
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
