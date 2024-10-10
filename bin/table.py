import abc

from prettytable import PrettyTable


class BasicTable(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_table(data: dict["subjects": list[str], "marks": list[tuple], "sr_marks": list[int]]) -> str:
        pass


class Table(BasicTable):
    @staticmethod
    def create_table(data: dict["subjects": list[str], "marks": list[tuple], "sr_marks": list[int]]) -> str:
        table = PrettyTable()
        table.add_column("Предмет", data["subjects"])
        table.add_column("Оценки", [' '.join(marks) for marks in data["marks"]])
        table.add_column("Средний балл", data["sr_marks"])
        return str(table)
