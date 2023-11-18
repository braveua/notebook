import oracledb  # https://www.oracle.com/database/technologies/appdev/python/quickstartpythononprem.html
from settings import dbc

class Notebook:
    def __init__(self):
        try:
            self.db = oracledb.connect(dsn='XEPDB1', user='CREATOR', password='qwe', config_dir='/opt/oracle/instantclient_21_12/network/admin')
        except oracledb.DatabaseError as ex:
            print(f"[Error] {ex}")
            # ex, = ex.args
            # print("Error Code:", ex.code)
            # print("Error Full Code:", ex.full_code)
            # print("Error Message:", ex.message)
        self.load_tags()

    def load_tags(self):
        try:
            with self.db.cursor() as cursor:
                cursor.execute("select * from tag")
                t = cursor.fetchall()
                self.tags = {}
                for i in t:
                    # print(i)
                    self.tags[i[0]] = i[1]
        except oracledb.DatabaseError as ex:
            print('Insert Error:', ex)

    def get_tags(self, tag_):
        res = []
        # tag_ = int(tag_)
        for bit in range(0, 16):
            if tag_ & (1 << bit):
                # print(bit)
                # print(self.tags)
                res.append(self.tags[bit])
        return res

    def show_all(self):
        try:
            with (self.db.cursor() as cursor):
                qry = 'SELECT * FROM note'
                cursor.execute(qry)
                resp = cursor.fetchall()
                for rec in resp:
                    rec = list(rec)
                    rec[5] = self.get_tags(rec[5])
                    print(rec)
                    # print(rec, self.get_tags(rec["tag"]))
        except oracledb.DatabaseError as ex:
            print('Error:', ex)

    def get_notes(self):
        try:
            with (self.db.cursor() as cursor):
                qry = 'SELECT * FROM note'
                cursor.execute(qry)
                resp = cursor.fetchall()
                # print(resp)
                res = []
                for rec in resp:
                    rec = list(rec)
                    # rec[5] = self.get_tags(rec[5])
                    drec = {"id": rec[0],
                            "parentid": rec[1],
                            "subject": rec[2],
                            "content": rec[3],
                            "ts": rec[4],
                            "tag": rec[5]}
                    res.append(drec)

        except oracledb.DatabaseError as ex:
            print('Error:', ex)
        return res

    def add_note(self, subject, parentid=None, id_=None, content=None, tag=0):
        try:
            with self.db.cursor() as cursor:
                cursor.callproc("nb.addnote", (id_, parentid, subject, content, tag))
                self.db.commit()
                print(f"[INFO] 1 row inserted.")
        except oracledb.DatabaseError as ex:
            print('Insert Error:', ex)

    def update_note(self, id_, subject, content):
        try:
            with self.db.cursor() as cursor:
                cursor.callproc("nb.updatenote", (id_, subject, content))
                self.db.commit()
        except oracledb.DatabaseError as ex:
            print('Update Error:', ex)

    def del_note(self, id_):
        try:
            with self.db.cursor() as cursor:
                cursor.callproc("nb.deletenote", (id_,))
                self.db.commit()
        except oracledb.DatabaseError as ex:
            print('Delete Error:', ex)


if __name__ == "__main__":
    nb = Notebook()
    # nb.add_note("Записка #3", tag=12)
    # nb.add_note("Записка #2")
    # nb.add_note(parentid=1, subject="пункт 1", content="описание")
    # nb.show_all()
    # print(nb.get_tags(62))
