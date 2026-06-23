from datetime import datetime
from typing import List, Optional
from .readable import Readable
from .reading_log import Readinglog

class Book(Readable):
    def __init__(self, title: str, author: str, genre: str, pages: int, 
                 added_date: Optional[str] = None):
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = pages
        self.added_date = added_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reading_logs: List[Readinglog] = []
        self.is_completed = False
        self.total_pages_read = 0
        self.book_type = "Book"
    
    def get_info(self): # type: ignore
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'pages': self.pages,
            'added_date': self.added_date,
            'completed': self.is_completed,
            'total_pages_read': self.total_pages_read,
            'progress': self.get_proggres()
        }
    
    def get_proggres(self):
        if self.pages == 0:
            return 0.0
        return round((self.total_pages_read / self.pages) * 100, 1)
    
    def add_reading_log(self, log: Readinglog):
        self.reading_logs.append(log)
        self.total_pages_read += log.pages_read
        if self.total_pages_read >= self.pages:
            self.is_completed = True
    
    def __str__(self):
        return f"{self.title} by {self.author} ({self.genre})"