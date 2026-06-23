import sys
from models import Book, EBook, AudioBook
from services import ReadingTracker
from storage import DataExporter
from exceptions import BookNotFoundError, InvalidLogError, FileOperationError


def main():
    
    tracker = ReadingTracker()
    exporter = DataExporter()
    running = True
    
    print("\n" + "="*50)
    print("WELCOME TO BOOKBUDDY")
    print("="*50)
    
    while running:
        print("\n" + "-"*50)
        print("MAIN MENU")
        print("-"*50)
        print("1. Add Book")
        print("2. View All Books")
        print("3. Add Reading Session")
        print("4. View Reading Progress")
        print("5. Export Data")
        print("6. Import Data")
        print("7. View Book Details")
        print("8. Exit")
        print("-"*50)
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            print("\n" + "-"*50)
            print("ADD A NEW BOOK")
            print("-"*50)
            
            try:
                title = input("Enter book title: ").strip()
                if not title:
                    print("[ERROR] Title cannot be empty")
                    continue
                
                author = input("Enter author name: ").strip()
                if not author:
                    print("[ERROR] Author cannot be empty")
                    continue
                
                genre = input("Enter genre: ").strip()
                if not genre:
                    print("[ERROR] Genre cannot be empty")
                    continue
                
                pages = input("Enter total pages: ").strip()
                try:
                    pages = int(pages)
                    if pages <= 0:
                        print("[ERROR] Pages must be greater than 0")
                        continue
                except ValueError:
                    print("[ERROR] Please enter a valid number")
                    continue
                
                print("\nBook type:")
                print("1. Regular Book")
                print("2. EBook")
                print("3. AudioBook")
                book_type = input("Choose book type (1-3): ").strip()
                
                if book_type == "1":
                    book = Book(title, author, genre, pages)
                elif book_type == "2":
                    file_format = input("Enter file format (e.g., PDF, EPUB): ").strip()
                    if not file_format:
                        file_format = "PDF"
                    
                    file_size = input("Enter file size (MB): ").strip()
                    try:
                        file_size = float(file_size) if file_size else 0
                    except ValueError:
                        file_size = 0
                    
                    book = EBook(title, author, genre, pages, file_format, file_size)
                elif book_type == "3":
                    narrator = input("Enter narrator name: ").strip()
                    duration = input("Enter duration (minutes): ").strip()
                    try:
                        duration = int(duration) if duration else 0
                    except ValueError:
                        duration = 0
                    
                    book = AudioBook(title, author, genre, pages, narrator, duration)
                else:
                    print("[ERROR] Invalid book type. Using regular book.")
                    book = Book(title, author, genre, pages)
                
                tracker.add_book(book)
                
            except Exception as e:
                print(f"[ERROR] Failed to add book: {e}")
        
        elif choice == "2":
            print("\n" + "-"*50)
            print("ALL BOOKS IN LIBRARY")
            print("-"*50)
            
            books = tracker.get_all_books()
            
            if not books:
                print("No books in your library yet!")
            else:
                for i, book in enumerate(books, 1):
                    progress = book.get_proggres()
                    status = "[DONE]" if book.is_completed else "[...]"
                    print(f"{i}. {status} {book.title} - {book.author} ({book.genre})")
                    print(f"   Pages: {book.total_pages_read}/{book.pages} ({progress}%)")
                    print()
        
        elif choice == "3":
            print("\n" + "-"*50)
            print("ADD READING SESSION")
            print("-"*50)
            
            if not tracker.get_all_books():
                print("[ERROR] No books in library. Please add a book first.")
                continue
            
            # Show available books
            books = tracker.get_all_books()
            for i, book in enumerate(books, 1):
                print(f"{i}. {book.title}")
            
            print("-"*50)
            title = input("Enter book title: ").strip()
            if not title:
                print("[ERROR] Title cannot be empty")
                continue
            
            try:
                pages = input("Enter pages read: ").strip()
                try:
                    pages = int(pages)
                    if pages <= 0:
                        print("[ERROR] Pages must be greater than 0")
                        continue
                except ValueError:
                    print("[ERROR] Please enter a valid number")
                    continue
                
                notes = input("Enter notes (optional): ").strip()
                
                tracker.add_reading_session(title, pages, notes)
                
            except BookNotFoundError as e:
                print(f"[ERROR] {e}")
            except InvalidLogError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] Failed to add reading session: {e}")
        
        elif choice == "4":
            print("\n" + "-"*50)
            print("VIEW READING PROGRESS")
            print("-"*50)
            tracker.display_progress()
        
        elif choice == "5":
            print("\n" + "-"*50)
            print("EXPORT DATA")
            print("-"*50)
            
            if not tracker.get_all_books():
                print("[ERROR] No books to export.")
                continue
            
            print("Available formats:")
            print("1. JSON")
            print("2. Pickle")
            
            format_choice = input("Choose format (1-2): ").strip()
            
            if format_choice == "1":
                format_type = "json"
            elif format_choice == "2":
                format_type = "pickle"
            else:
                print("[ERROR] Invalid format")
                continue
            
            filename = input("Enter filename (without extension): ").strip()
            if not filename:
                print("[ERROR] Filename cannot be empty")
                continue
            
            filename = f"{filename}.{format_type}"
            
            try:
                books = tracker.get_all_books()
                exporter.export_data(books, filename, format_type)
                
            except FileOperationError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] Failed to export data: {e}")
        
        elif choice == "6":
            print("\n" + "-"*50)
            print("IMPORT DATA")
            print("-"*50)
            
            filename = input("Enter filename to import: ").strip()
            if not filename:
                print("[ERROR] Filename cannot be empty")
                continue
            
            import os
            if not os.path.exists(filename):
                print(f"[ERROR] File '{filename}' not found")
                continue
            
            try:
                # Check if we should replace or append
                if tracker.get_all_books():
                    answer = input("Replace all existing data? (y/n): ").strip().lower()
                    if answer in ['y', 'yes']:
                        tracker = ReadingTracker()
                
                books = exporter.import_data(filename)
                
                for book in books:
                    tracker.add_book(book)
                
            except FileOperationError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] Failed to import data: {e}")
        
        elif choice == "7":
            print("\n" + "-"*50)
            print("BOOK DETAILS")
            print("-"*50)
            
            if not tracker.get_all_books():
                print("[ERROR] No books in library.")
                continue
            
            books = tracker.get_all_books()
            for i, book in enumerate(books, 1):
                progress = book.get_proggres()
                status = "[DONE]" if book.is_completed else "[...]"
                print(f"{i}. {status} {book.title} - {book.author}")
            
            print("-"*50)
            title = input("Enter book title: ").strip()
            if not title:
                print("[ERROR] Title cannot be empty")
                continue
            
            try:
                book = tracker.find_book(title)
                info = book.get_info()
                
                print("\n" + "="*50)
                print(f"Book: {info['title']}")
                print("="*50)
                print(f"Author: {info['author']}")
                print(f"Genre: {info['genre']}")
                print(f"Pages: {info['pages']}")
                print(f"Added: {info['added_date']}")
                print(f"Status: {'Completed' if info['completed'] else 'In Progress'}")
                print(f"Progress: {info['total_pages_read']}/{info['pages']} ({info['progress']}%)")
                
                if hasattr(book, 'book_type'):
                    print(f"Type: {book.book_type}")
    
                    if isinstance(book, EBook):
                        print(f"Format: {book.file_format}")
                        print(f"File Size: {book.file_size_mb} MB")
    
                    elif isinstance(book, AudioBook):
                        if book.narrator:
                             print(f"Narrator: {book.narrator}")
                             print(f"Duration: {book.duration_minutes} minutes")
                else:
                    print("Type: Book")

                if book.reading_logs:
                    print(f"\nReading Sessions: {len(book.reading_logs)}")
                    print("-"*30)
                    for i, log in enumerate(book.reading_logs[-5:], 1):
                        print(f"  {i}. {log.date}: {log.pages_read} pages")
                        if log.notes:
                            print(f"     Notes: {log.notes}")
                    if len(book.reading_logs) > 5:
                        print(f"  ... and {len(book.reading_logs) - 5} more sessions")
                else:
                    print("\nNo reading sessions recorded yet.")
                
                print("="*50)
                
            except BookNotFoundError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] Failed to get book details: {e}")
        
        elif choice == "8":
            print("\n" + "="*50)
            print("Goodbye! Happy reading!")
            print("="*50)
            running = False
        
        else:
            print("[ERROR] Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Program interrupted by user")
        print("Goodbye!")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)