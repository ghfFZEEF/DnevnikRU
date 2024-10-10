from bs4 import BeautifulSoup as bs
from bs4.element import Tag
import abc


class BasicHTML(abc.ABC):
    @abc.abstractmethod
    def get_subjects_marks_sr_murk(self, html: str) -> dict[list["subjects": str], list["marks": tuple], list["sr_marks": int]]:
        pass


class HTML(BasicHTML):
    def get_subjects_marks_sr_murk(self, html: str) -> dict[list["subjects": str], list["marks": tuple], list["sr_marks": int]]: 
        subjects_marks_sr_murk: dict = {"subjects": [], "marks": [], "sr_marks": []}
        soup_list: list = self.__get_soup_list(html=html)
        
        soup: bs
        for soup in soup_list:
            subject: str = self.__get_subject(soup=soup)
            marks: tuple = self.__get_marks(soup=soup)
            sr_murk: int = self.__get_sr_murk(soup=soup)
            
            subjects_marks_sr_murk["subjects"].append(subject)
            subjects_marks_sr_murk["marks"].append(marks)
            subjects_marks_sr_murk["sr_marks"].append(sr_murk)
        
        return subjects_marks_sr_murk
        

    @staticmethod
    def __get_subject(soup: bs) -> str:
        subject = soup.find("div", {"class": "c8D3G"})
        if subject is not None:
            return subject.text
        raise Exception("неверный html")


    @staticmethod
    def __get_marks(soup: bs) -> tuple:
        marks = soup.find("div", {"class": "Y1p7l"})
        if marks is not None:
            marks = marks.find_all("div" , recursive=False)
            if marks[0].text[-1] != 'к':
                return ([murk.text[-1] for murk in marks])
            else:
                return (marks[0].text,)
        raise Exception("неверный html")


    @staticmethod
    def __get_sr_murk(soup: bs) -> int:
        murk = soup.find_all("td")[2]
        if murk is not None:
            return murk.text
        raise Exception("неверный html")


    @staticmethod
    def __get_soup_list(html: str) -> list[Tag]:
        soup = bs(html, features="lxml")
        soup = soup.find_all("tr")[1:]
        return soup
    