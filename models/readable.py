from abc import ABC , abstractmethod

class Readable(ABC):

    @abstractmethod
    def get_info(self) -> dict:
        ...
        
    @abstractmethod
    def get_proggres(self) -> float:
        ...