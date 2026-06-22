from abc import ABC , abstractmethod

class Readable(ABC):

    @abstractmethod
    def get_info(self) -> str:
        ...
        
    @abstractmethod
    def get_proggres(self) -> float:
        ...