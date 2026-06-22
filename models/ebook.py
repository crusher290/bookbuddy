from book import Book

class Ebook(Book):
    def __init__(self, title: str, author: str, genre: str, total_pages: int, file_format, file_size):
        super().__init__(title, author, genre, total_pages)
        self.file_format = file_format
        self.file_size = file_size
    
    def get_info(self) -> str:
        return super().get_info()
    
    def get_proggres(self) -> float:
        return super().get_proggres()
    
    def update_proggres(self, page_read: int):
        return super().update_proggres(page_read)