import pymysql
from settings import dbc

tags = {"0": "Task",
        "1": "Linux",
        "2": "MySql",
        "3": "Python"}


class Notebook:
    def __init__(self):
        dbc["cursorclass"] = pymysql.cursors.DictCursor
        try:
            self.db = pymysql.connect(**dbc)
        except pymysql.err.OperationalError as ex:
            print('Error:', ex)
            exit()

    def get_tags(self, tag_):
        res = []
        for bit in range(0, 16):
            if tag_ & (1 << bit):
                res.append(tags[str(bit)])
        return res

    def show_all(self):
        try:
            with self.db.cursor() as cursor:
                qry = 'SELECT * FROM note'
                cursor.execute(qry)
                resp = cursor.fetchall()
                for rec in resp:
                    rec = dict(rec)
                    print(rec, self.get_tags(rec["tag"]))
        except pymysql.err.ProgrammingError as ex:
            print('Error:', ex)

    def add_note(self, subject, parentid=None, id_=None, content=None, tag=0):

        try:
            with self.db.cursor() as cursor:
                cursor.callproc("addnote", (id_, parentid, subject, content, tag))
                self.db.commit()
        except pymysql.err.ProgrammingError as ex:
            print('Insert Error:', ex)


if __name__ == "__main__":
    nb = Notebook()
    # nb.add_note("Записка #1")
    # nb.add_note("Записка #2")
    # nb.add_note(parentid=1, subject="пункт 1", content="описание")
    nb.show_all()

