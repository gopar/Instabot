# std libs
import sqlite3 as lite
from datetime import datetime


################################################################################
class DB(object):
    """ Class that connects to a Database """
    def __init__(self, db=None, table_name=None):
        super(DB, self).__init__()
        db = "insta.db" if db is None else db
        self.table_name = "insta_media" if table_name is None else table_name

        self._conn = lite.connect(db)
        self._cursor = self._conn.cursor()

        self.__createTableIfNotExists()

    # --------------------------------------------------------------------------
    def __createTableIfNotExists(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        results = self._cursor.execute(query.format(self.table_name))
        name_list = [name for r in results for name in r]

        if self.table_name not in name_list:
            table = """CREATE TABLE {}
                    (media TEXT PRIMARY KEY,
                    thumbnail TEXT, regular TEXT, large TEXT,
                    [timestamp] timestamp)
                   """.format(self.table_name)
            self._cursor.execute(table)

    # --------------------------------------------------------------------------
    def insertValues(self, _id, thumbnail, regular, large):
        query = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            self.table_name, _id, thumbnail, regular, large, datetime.now()
        )
        self._cursor.execute(query)
        self._conn.commit()

    # --------------------------------------------------------------------------
    def isKeyInDB(self, pk):
        query = "SELECT media FROM {}".format(self.table_name)
        results = self._cursor.execute(query)
        pk_list = [_pk for r in results for _pk in r]

        for _pk in pk_list:
            if pk == _pk:
                return True
        return False
