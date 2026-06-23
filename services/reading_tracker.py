from typing import List, Dict, Any, Optional
from models import Book, Readinglog
from exceptions import BookNotFoundError, InvalidLogError
from utils import log_book_action, log_error_with_context


class ReadingTracker:
    
    def __init__(self):
        self.books: List[Book] = []
    
    def add_book(self, book: Book) -> None:
        self.books.append(book)
        log_book_action("ADDED", book.title)
        print(f"[SUCCESS] Book '{book.title}' added to your library")
    
    def find_book(self, title: str) -> Book:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        raise BookNotFoundError(title)
    
    def get_all_books(self) -> List[Book]:
        return self.books
    
    def get_book_count(self) -> int:
        return len(self.books)
    
    def add_reading_session(self, title: str, pages_read: int, notes: str = "") -> None:
        if pages_read <= 0:
            raise InvalidLogError("Pages read must be greater than 0")
        
        book = self.find_book(title)
        
        
        remaining_pages = book.pages - book.total_pages_read
        if pages_read > remaining_pages:
            raise InvalidLogError(f"Cannot read {pages_read} pages. Only {remaining_pages} pages remaining")
        
        
        log = Readinglog(pages_read=pages_read, notes=notes)
        book.add_reading_log(log)
        
        log_book_action("READING", f"{title} - {pages_read} pages")
        print(f"[SUCCESS] Reading session added for '{title}'")
    
    def get_proggres(self, title: str) -> Dict[str, Any]:
        
        book = self.find_book(title)
        info = book.get_info()
        
        return {
            'title': info['title'],
            'pages_read': info['total_pages_read'],
            'total_pages': info['pages'],
            'progress_percentage': info['progress'],
            'completed': info['completed'],
            'logs_count': len(book.reading_logs)
        }
    
    def get_all_progress(self) -> List[Dict[str, Any]]:
        
        progress_list = []
        for book in self.books:
            progress_list.append(self.get_proggres(book.title))
        return progress_list
    
    def display_progress(self) -> None:
        if not self.books:
            print("\n[INFO] No books in your library yet!")
            return
        
        print("\n" + "="*60)
        print("📚 YOUR READING PROGRESS")
        print("="*60)
        
        completed_count = sum(1 for book in self.books if book.is_completed)
        print(f"Total Books: {len(self.books)}")
        print(f"Completed: {completed_count}")
        print("-"*60)
        
        for book in self.books:
            progress = book.get_proggres()
            status = "✅ COMPLETED" if book.is_completed else "⏳ IN PROGRESS"
            bar = self._create_progress_bar(progress)
            
            print(f"\n📖 {book.title}")
            print(f"   Author: {book.author}")
            print(f"   Pages: {book.total_pages_read}/{book.pages} ({progress}%)")
            print(f"   Status: {status}")
            print(f"   {bar}")
            

            if book.reading_logs:
                latest = book.reading_logs[-1]
                print(f"   Last session: {latest.pages_read} pages on {latest.date}")
        
        print("\n" + "="*60)
    
    def _create_progress_bar(self, progress: float, width: int = 30) -> str:
        filled = int((progress / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {progress}%"
    
    def get_completed_books(self) -> List[Book]:
        return [book for book in self.books if book.is_completed]
    
    def get_in_progress_books(self) -> List[Book]:
        return [book for book in self.books if not book.is_completed and book.total_pages_read > 0]
    
    def get_unread_books(self) -> List[Book]:
        return [book for book in self.books if book.total_pages_read == 0]