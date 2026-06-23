from typing import List, Any
from models import Book
from exceptions import DataExportError, DataImportError
from utils import log_file_action, log_error_with_context
from .json_handler import JSONHandler 
from storage.pickle_handler import PickleHandler


class DataExporter:
    
    def __init__(self):
        self.json_handler = JSONHandler()
        self.pickle_handler = PickleHandler()
        self.supported_formats = ['json', 'pickle']
    
    def export_data(self, books: List[Book], filename: str, format_type: str = 'json') -> None:
        if format_type not in self.supported_formats:
            raise DataExportError(f"Unsupported format: {format_type}")
        
        if not filename:
            raise DataExportError("Filename cannot be empty")
        
        try:
            if format_type == 'json':
                self.json_handler.save(books, filename)
            elif format_type == 'pickle':
                self.pickle_handler.save(books, filename)
            
            log_file_action("EXPORTED", filename)
            print(f"[SUCCESS] Data exported to '{filename}'")
            
        except Exception as e:
            log_error_with_context(e, "Export failed")
            raise DataExportError(f"Failed to export data: {str(e)}")
    
    def import_data(self, filename: str) -> List[Book]:
        if not filename:
            raise DataImportError("Filename cannot be empty")
        
        try:
            if filename.endswith('.json'):
                books = self.json_handler.load(filename)
            elif filename.endswith('.pickle') or filename.endswith('.pkl'):
                books = self.pickle_handler.load(filename)
            else:
                raise DataImportError(f"Unsupported file format: {filename}")
            
            log_file_action("IMPORTED", filename)
            print(f"[SUCCESS] Imported {len(books)} books from '{filename}'")
            return books
            
        except Exception as e:
            log_error_with_context(e, "Import failed")
            raise DataImportError(f"Failed to import data: {str(e)}")