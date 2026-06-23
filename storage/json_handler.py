import json
from typing import List, Dict, Any
from models import Book, EBook, AudioBook, Readinglog
from exceptions import FileOperationError
from utils import safe_file_open


class JSONHandler:
    
    def save(self, books: List[Book], filename: str) -> None:
        data = []
        for book in books:
            book_data = book.get_info()
            book_data['book_type'] = book.__class__.__name__
            
            # Add reading logs
            logs = []
            for log in book.reading_logs:
                logs.append(log.get_info())
            book_data['reading_logs'] = logs
            
            data.append(book_data)
        
        try:
            with safe_file_open(filename, 'w') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except Exception as e:
            raise FileOperationError(filename, f"Failed to save JSON: {str(e)}")
    
    def load(self, filename: str) -> List[Book]:
        try:
            with safe_file_open(filename, 'r') as file:
                data = json.load(file)
            
            books = []
            for item in data:
                book = self._create_book_from_dict(item)
                books.append(book)
            
            return books
            
        except json.JSONDecodeError as e:
            raise FileOperationError(filename, f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise FileOperationError(filename, f"Failed to load JSON: {str(e)}")
    
    def _create_book_from_dict(self, data: Dict[str, Any]) -> Book:
        book_type = data.get('book_type', 'Book')
        

        constructor_data = {
            'title': data.get('title', 'Unknown'),
            'author': data.get('author', 'Unknown'),
            'genre': data.get('genre', 'Unknown'),
            'pages': data.get('pages', 0),
            'added_date': data.get('added_date')
        }
        
        if book_type == 'EBook':
            constructor_data['file_format'] = data.get('file_format', 'PDF')
            constructor_data['file_size_mb'] = data.get('file_size_mb', 0)
            book = EBook(**constructor_data)
        elif book_type == 'AudioBook':
            constructor_data['narrator'] = data.get('narrator', '')
            constructor_data['duration_minutes'] = data.get('duration_minutes', 0)
            book = AudioBook(**constructor_data)
        else:
            book = Book(**constructor_data)
        
        # Add reading logs
        for log_data in data.get('reading_logs', []):
            log = Readinglog(
                date=log_data.get('date'),
                pages_read=log_data.get('pages_read', 0),
                notes=log_data.get('notes', '')
            )
            book.add_reading_log(log)
        
        return book