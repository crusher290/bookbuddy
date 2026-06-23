import pickle
from typing import List
from models import Book
from exceptions import FileOperationError
from utils import safe_file_open


class PickleHandler:
    
    
    def save(self, books: List[Book], filename: str) -> None:
        
        try:
            with safe_file_open(filename, 'wb') as file:
                pickle.dump(books, file)
        except Exception as e:
            raise FileOperationError(filename, f"Failed to save pickle: {str(e)}")
    
    def load(self, filename: str) -> List[Book]:
        
        try:
            with safe_file_open(filename, 'rb') as file:
                data = pickle.load(file)
            
            
            if not isinstance(data, list):
                raise FileOperationError(filename, "Invalid data format: expected list")
            
            
            for item in data:
                if not isinstance(item, Book):
                    raise FileOperationError(filename, "Invalid data: contains non-book objects")
            
            return data
            
        except pickle.UnpicklingError as e:
            raise FileOperationError(filename, f"Invalid pickle format: {str(e)}")
        except Exception as e:
            raise FileOperationError(filename, f"Failed to load pickle: {str(e)}")