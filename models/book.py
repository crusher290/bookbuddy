from readable import Readable

class Book(Readable):
    def __init__(self, title:str, author:str, genre:str, total_pages:int):
        self.title = title
        self.author = author
        self.genre = genre
        self.total_pages = total_pages
        self.current_page = 0

    @property
    def get_info(self) -> str:
        return f"{self.title} by {self.author} - [genre : {self.genre}] - ({self.total_pages} pages)"
    
    def get_proggres(self) -> float:
        if self.current_page == 0:
            return 0.0
        proggres = (self.current_page / self.total_pages) * 100
        return f"{proggres:,.2f}"
        
    
    def update_proggres(self, page_read:int):
        if page_read < 0 :
            raise ValueError
        self.current_page += page_read
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages





b = Book("habits","ali","self-help",200)  

print(b.get_info)

b.update_proggres(100)

print(b.get_proggres())