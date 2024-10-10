import abc
from sqlite3 import connect, Connection, Cursor


class BasicDb(abc.ABC):
    @abc.abstractmethod
    def __init__(self, data_path: str) -> None:
        pass
    
    @abc.abstractmethod
    def create_data_table(self) -> None:
        pass
     
    @abc.abstractmethod
    def create_new_user(self, id: int, login: str, password: str) -> None:
        pass
    
    @abc.abstractmethod
    def update_log_pas(self, id: int, login: str, password: str) -> None:
        pass
    
    @abc.abstractmethod
    def update_school_schooler_num(self, id: int, school_schooler_num: tuple["school_num": int, "schooler_num": int]) -> None:
        pass
    
    @abc.abstractmethod
    def get_log_pas(self, id: int) -> tuple["login": str, "password": str]:
        pass
    
    @abc.abstractmethod
    def get_school_schooler_num(self, id: int) -> tuple["school_num": int, "schooler_num": int]:
        pass
    
    @abc.abstractmethod
    def user_in_table(self, id: int) -> bool:
        pass


class Db(BasicDb):
    def __init__(self, data_path: str) -> None:
        self.__path = data_path
        
    
    def create_data_table(self) -> None:
        db: Connection = connect(f"{self.__path}/users.db")
        cursor: Cursor = db.cursor()
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS data (
                        id INTEGER,
                        password TEXT,
                        login TEXT,
                        school_num INTEGER,
                        schooler_num INTEGER
                    )""")
        db.commit()
        
        cursor.close()
        db.close()
     
    def create_new_user(self, id: int, login: str, password: str) -> None:
        db: Connection = connect(f"{self.__path}/users.db")
        cursor: Cursor = db.cursor()
        
        cursor.execute("INSERT INTO data (id, password, login) VALUES ('%s', '%s', '%s')" % (id, password, login))
        db.commit()
        
        cursor.close()
        db.close()
     
     
    def update_log_pas(self, id: int, login: str, password: str) -> None:
        db: Connection = connect(f"{self.__path}/users.db")
        cursor: Cursor = db.cursor()

        cursor.execute("UPDATE data SET login = '%s', password = '%s' WHERE id = '%s'" % (login, password, id))
        db.commit()
        
        cursor.close()
        db.close()
    
    def update_school_schooler_num(self, id: int, school_schooler_num: tuple["school_num": int, "schooler_num": int]) -> None:
        db: Connection = connect(f"{self.__path}/users.db")
        cursor: Cursor = db.cursor()

        school_num: int = school_schooler_num[0]
        schooler_num = school_schooler_num[1]
        
        cursor.execute("UPDATE data SET school_num = '%s', schooler_num = '%s' WHERE id = '%s'" % (school_num, schooler_num, id))
        db.commit()
        
        cursor.close()
        db.close()
   
    
    def get_log_pas(self, id: int) -> tuple["login": str, "password": str]:
        db: Connection = connect(f"{self.__path}/users.db")
        cursor: Cursor = db.cursor()
        
        login: str
        password: str

        cursor.execute("SELECT login, password FROM data WHERE id = '%s'" % id)
        login, password = cursor.fetchone()
            
        cursor.close()
        db.close()

        return (login, password)
    
    def get_school_schooler_num(self, id: int) -> tuple["school_num": int, "schooler_num": int]:
        db: Connection = connect(f"{self.__path}/users.db")
        cursor: Cursor = db.cursor()
        
        school_num: int
        schooler_num: int
        cursor.execute("SELECT school_num, schooler_num FROM data WHERE id = '%s'" % id)
        school_num, schooler_num = cursor.fetchone()
        
        cursor.close()
        db.close()

        return (school_num, schooler_num)
    
    
    def user_in_table(self, id: int) -> bool:
        db: Connection = connect(f"{self.__path}/users.db")
        cursor: Cursor = db.cursor()
        
        cursor.execute("SELECT id FROM data WHERE id = '%s'" % id)
        data: int = cursor.fetchone()
        
        cursor.close()
        db.close()

        return data is not None
    