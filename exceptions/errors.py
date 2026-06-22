class BookBuddyError(Exception):
    pass


class BookNotFoundError(BookBuddyError): # it will raised when a book not found
    def __init__(self, title: str = ""):
        self.title = title
        if title:
            error_message = f"Book '{title}' not found in library"
        else:
            error_message = "Book not found"
        super().__init__(error_message)


class InvalidLogError(BookBuddyError):# it wil raised when a readin_log is invalid
    def __init__(self, message: str = "Invalid reading log entry"):
        self.message = message
        super().__init__(message)


class FileOperationError(BookBuddyError): # it will raised when file operation fail
    def __init__(self, filename: str = "", message: str = ""):
        self.filename = filename
        if message:
            error_message = f"File operation failed: {message}"
        else:
            error_message = f"File operation failed for '{filename}'"
        super().__init__(error_message)


class DataExportError(BookBuddyError): # it will raised when data export fails
    def __init__(self, message: str = "Failed to export data"):
        self.message = message
        super().__init__(message)


class DataImportError(BookBuddyError): # it will raised when data import fails
    def __init__(self, message: str = "Failed to import data"):
        self.message = message
        super().__init__(message)


class ValidationError(BookBuddyError): # it will raised when data validation fails
    def __init__(self, field: str = "", message: str = ""):
        self.field = field
        if field and message:
            error_message = f"Validation failed for '{field}': {message}"
        elif field:
            error_message = f"Validation failed for '{field}'"
        elif message:
            error_message = f"Validation failed: {message}"
        else:
            error_message = "Validation failed"
        super().__init__(error_message)