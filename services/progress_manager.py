from typing import List, Dict, Any
from models import Book, Readinglog
from exceptions import BookNotFoundError, InvalidLogError


class ProgressManager:
    
    def __init__(self):
        self.books: List[Book] = []
    
    def add_book(self, book: Book) -> None:
        self.books.append(book)
        print(f"[SUCCESS] Book '{book.title}' added to library")
    
    def find_book(self, title: str) -> Book:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        raise BookNotFoundError(title)
    
    def get_all_books(self) -> List[Book]:
        return self.books
    
    def add_reading_log(self, title: str, pages_read: int, notes: str = "") -> None:
        if pages_read <= 0:
            raise InvalidLogError("Pages read must be greater than 0")
        
        book = self.find_book(title)
        
        if book.total_pages_read + pages_read > book.pages:
            remaining = book.pages - book.total_pages_read
            raise InvalidLogError(f"Cannot read {pages_read} pages. Only {remaining} pages remaining")
        
        log = Readinglog(pages_read=pages_read, notes=notes)
        book.add_reading_log(log)
        print(f"[SUCCESS] Reading log added for '{title}'")
    
    def get_progress_summary(self) -> Dict[str, Any]:
        total_books = len(self.books)
        completed_books = sum(1 for book in self.books if book.is_completed)
        
        summary = {
            'total_books': total_books,
            'completed_books': completed_books,
            'completion_rate': f"{round((completed_books / total_books) * 100, 1)}%" if total_books > 0 else "0%",
            'books': []
        }
        
        for book in self.books:
            info = book.get_info()
            summary['books'].append({
                'title': info['title'],
                'pages_read': info['total_pages_read'],
                'total_pages': info['pages'],
                'progress': info['progress'],
                'completed': info['completed']
            })
        
        return summary
    
    def display_progress(self) -> None:
        summary = self.get_progress_summary()
        
        print("\n" + "="*50)
        print("READING PROGRESS SUMMARY")
        print("="*50)
        print(f"Total Books: {summary['total_books']}")
        print(f"Completed: {summary['completed_books']}")
        print(f"Completion Rate: {summary['completion_rate']}")
        print("-"*50)
        
        if summary['books']:
            for book in summary['books']:
                status = "✅ COMPLETED" if book['completed'] else "⏳ IN PROGRESS"
                print(f"{book['title']} - {book['pages_read']}/{book['total_pages']} pages ({book['progress']}%) {status}")
        else:
            print("No books in library")
        print("="*50 + "\n")