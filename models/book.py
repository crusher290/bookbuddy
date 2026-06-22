from readable import Readable
from datetime import datetime

class Book(Readable):
    def __init__(self, title:str, author:str, genre:str, total_pages:int):
        self.title = title
        self.author = author
        self.genre = genre
        self.total_pages = total_pages
        self.date_added = datetime.now().strftime("%y/%m/%d,%H:%M:%S")
        self.__current_page = 0

    
    def get_info(self) -> str:
        return f"{self.title} by {self.author} - [genre : {self.genre}] - ({self.total_pages} pages)"
    
    def get_proggres(self) -> float:
        if self.__current_page == 0:
            return 0.0
        proggres = (self.__current_page / self.total_pages) * 100
        return f"{proggres:,.2f}"
        
    
    def update_proggres(self, page_read:int):
        if page_read < 0 :
            raise ValueError("You Can't enter negitive number.")
        self.__current_page += page_read
        if self.__current_page > self.total_pages:
            self.__current_page = self.total_pages





b = Book("habits","ali","self-help",200)  

print(b.get_info())

b.update_proggres(101)

print(b.get_proggres())

