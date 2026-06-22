from datetime import datetime
from typing import Optional

class Reading_log:
    def __init__(self, date: Optional[str]= None, notes:str="", pages_read:int=0):
        self.date = date or datetime.now().strftime("%Y/%m/%d | %H:%M")
        self.notes = notes
        self.pages_read =pages_read


    def get_info(self):
        return {
            "date":self.date,
            "note":self.notes,
            "pages_read":self.pages_read
        }

    def __str__(self):
        return f"{self.date}: {self.pages_read} page - {self.notes[:30]}"