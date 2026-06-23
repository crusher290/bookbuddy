from .book import Book
from typing import Optional

class EBook(Book): 
    
    def __init__(self, title: str, author: str, genre: str, pages: int,
                 file_format: str = "PDF", file_size_mb: float = 0.0,
                 added_date: Optional[str] = None):
        super().__init__(title, author, genre, pages, added_date) 
        self.file_format = file_format
        self.file_size_mb = file_size_mb
        self.book_type = "EBook"
    
    def get_info(self):
        info = super().get_info()  
        info.update({
            'book_type': self.book_type,
            'file_format': self.file_format,
            'file_size_mb': self.file_size_mb
        })
        return info
