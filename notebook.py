import pymysql


class Notebook:
    dbc = {"host": "filesrv",
           "database": "notebook",
           "user": "creator",
           "password": "qwe",
           # "cursorclass": pymysql.cursors.DictCursor
           }

    def __init__(self):
        try:
            self.db = pymysql.connect(**self.dbc)
        except pymysql.err.OperationalError as ex:
            print('Error:', ex)
            exit()

    def show_all(self):
        try:
            with self.db.cursor() as cursor:
                qry = 'SELECT * FROM note'
                cursor.execute(qry)
                resp = cursor.fetchall()
                for rec in resp:
                    print(rec)
        except pymysql.err.ProgrammingError as ex:
            print('Error:', ex)

    def add_note(self, subject, parentid=None, id_=None, content=None):
        # self.db.cursor().execute("""
        #     CREATE TABLE IF NOT EXISTS note(
        #         id INT PRIMARY KEY AUTO_INCREMENT,
        #         parentid INT,
        #         subject VARCHAR(100),
        #         content TEXT,
        #         ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #     );
        # """)

        try:
            with self.db.cursor() as cursor:
                cursor.callproc("addnote", (id_, parentid, subject, content))
                self.db.commit()
        except pymysql.err.ProgrammingError as ex:
            print('Insert Error:', ex)


if __name__ == "__main__":
    nb = Notebook()
    nb.add_note("Записка #1")
    nb.add_note("Записка #2")
    nb.add_note(parentid=1, subject="пункт 1", content="описание")
    nb.show_all()
