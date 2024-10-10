import abc
from os import remove

from bin.parser import BasicParser
from bin.HTML_reader import BasicHTML
from bin.JSON import BasicJSON 
from bin.db_work import BasicDb


class BasicData(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def __init__(self, data_path: str, parser: BasicParser, html: BasicHTML, json: BasicJSON, db: BasicDb) -> None:
        pass
    
    @abc.abstractmethod
    def create_data(self, id: int) -> bool:
        pass
    
    @abc.abstractmethod
    def get_data(self, id: int) -> dict["subjects": list[str], "marks": list[tuple], "sr_marks": list[int]] | bool:
        pass
    
    @abc.abstractmethod
    def delete_cookies_marks_school_schooler_num(self, id: int) -> None:
        pass

 
class Data(BasicData):
    def __init__(self, data_path: str, parser: BasicParser, html: BasicHTML, json: BasicJSON, db: BasicDb) -> None:
        self.__path: str = data_path
        self.__json: BasicJSON = json(self.__path)
        xpath: dict["login": str, "password": str, "button": str, "period": str] = self.__json.get_xpath()
        self.__parser: BasicParser = parser(xpath)
        self.__html: BasicHTML = html()
        self.__db: BasicDb = db(self.__path)
    
    
    def create_data(self, id: int) -> bool:
        if not self.__db.user_in_table(id):
            return False
        
        cookies: list | bool = self.__json.get_cookies(id)
        html: str | bool = False
        if cookies:
            school_schooler_num: tuple = self.__db.get_school_schooler_num(id)
            html: str | bool = self.__parser.get_html(cookies, school_schooler_num)
        
        if not cookies or not html:
            login: str
            password: str
            login, password = self.__db.get_log_pas(id)
            response: tuple = self.__parser.get_cookies_school_schooler_num(login, password)
            if not response:
                return False 
            
            self.__json.save_cookies(id, response[0])
            self.__db.update_school_schooler_num(id, response[1])
            
            html: str | bool = self.__parser.get_html(response[0], response[1])
            
        if html:
            subject_marks_sr_murk: dict = self.__html.get_subjects_marks_sr_murk(html)
            self.__json.save_data(id, subject_marks_sr_murk)
            return True
        else:
            return False
        
        
    def get_data(self, id: int) -> dict["subjects": list[str], "marks": list[tuple], "sr_marks": list[int]] | bool:
        data: dict = self.__json.get_data(id)
        return data
    
    def delete_cookies_marks_school_schooler_num(self, id: int) -> None:
        try:
            remove(f"{self.__path}/cookies/{id}.json")
        except FileNotFoundError:
            pass
        
        try:
            remove(f"{self.__path}/person_data/{id}.json")
        except FileNotFoundError:
            pass
        
        self.__db.update_school_schooler_num(id, (None, None))
        
    