from .book import Book
from typing import Optional

class AudioBook(Book):  
    def __init__(self, title: str, author: str, genre: str, pages: int,
                 narrator: str = "", duration_minutes: int = 0,
                 added_date: Optional[str] = None):
        super().__init__(title, author, genre, pages, added_date)  
        self.narrator = narrator
        self.duration_minutes = duration_minutes
        self.book_type = "AudioBook"
    
    def get_info(self):
        info = super().get_info()  
        info.update({
            'book_type': self.book_type,
            'narrator': self.narrator,
            'duration_minutes': self.duration_minutes
        })
        return info
