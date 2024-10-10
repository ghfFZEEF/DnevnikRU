import abc
import json


class BasicJSON(abc.ABC):
    @abc.abstractmethod
    def __init__(self, data_path: str) -> None:
        pass
    
    @abc.abstractmethod
    def get_xpath(self) -> dict["login": str, "password": str, "button": str, "period": str]:
        pass

    @abc.abstractmethod
    def save_data(self, id: int, data: dict) -> None:
        pass

    @abc.abstractmethod
    def get_data(self, id: int) -> dict["subject": list[str], "sr_marks": list[tuple], "sr_marks": list[int]] | bool:
        pass

    @abc.abstractmethod
    def save_cookies(self, id: int, cookies: list[dict]) -> None: 
        pass
    
    @abc.abstractmethod
    def get_cookies(self, id: int) -> list[dict] | bool:
        pass
    
    @abc.abstractmethod
    def get_token(self) -> str:
        pass
    

class JSON(BasicJSON):    
    def __init__(self, data_path: str) -> None:
        self.__path: str = data_path
        
    def get_xpath(self) -> dict["login": str, "password": str, "button": str, "period": str]:
        with open(f"{self.__path}/urls.json") as file:
            urls: dict = json.loads(file.read())
        return urls["xpath"]
        
    def save_data(self, id: int, data: dict) -> None:
        with open(f"{self.__path}/person_data/{id}.json", 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
            
    def get_data(self, id: int) -> dict["subject": list[str], "sr_marks": list[tuple], "sr_marks": list[int]] | bool:
        try:
            with open(f"{self.__path}/person_data/{id}.json", encoding="utf-8") as file:
                return json.loads(file.read())
        except IOError:
            return False
        
    def get_token(self) -> str:
        with open(f"{self.__path}/token.json", 'r') as file:
            data: dict = json.load(file)
        token: str = data["token"]
        return token
    
    def save_cookies(self, id: int, cookies: list[dict]) -> None:
        with open(f"{self.__path}/cookies/{id}.json", 'w', encoding="utf-8") as file:
            json.dump(cookies, file)
    
    def get_cookies(self, id: int) -> list[dict] | bool:
        try:
            with open(f"{self.__path}/cookies/{id}.json", encoding="utf-8") as file:
                return json.loads(file.read())
        except IOError:
            return False
