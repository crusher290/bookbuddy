from book import Book

class Audiobook(Book)
    def __init__(self, title: str, author: str, genre: str, total_pages: int, duration, narrator):
        super().__init__(title, author, genre, total_pages)
        self.duration = duration 
        self.narrator = narrator
    
    def get_info(self) -> str:
        return super().get_info()
    
    def get_proggres(self) -> float:
        return super().get_proggres()
    
    def update_proggres(self, page_read: int):
        return super().update_proggres(page_read)