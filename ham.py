import hashlib, base64, datetime
import sqlite3 as sql


class Database:
    def __init__(self,db):
        self.db = db
        self.connection()
        
    def connection(self):
        conn = sql.connect(self.db)
        query = conn.cursor()
        
        return (conn, query)
    
    def findtable(self, table, rows = ''):
        conn, query = self.connection()
        try:
            query.execute(f"SELECT * FROM {table}")
            #print('Table exists.')

            return True
            
        except Exception as e:
            print(e)
            if rows:
                query.execute(rows)
                print("Table successfully created")

                return True

            else:
                return False
            
        conn.commit()
        conn.close()

    def findrow(self, sql, comp=""):
        conn, query = self.connection()
        try:
            query.execute(sql)
            rows = query.fetchall()   
            return rows
            
        except Exception as e:
            print(e)
            return False
            
        conn.commit()
        conn.close()
        

class Ham():
    def __init__(self):
        self.database = Database('database.db')
        self.dbconn, self.dbquery = self.database.connection()
        self.dbbankrows = "CREATE TABLE bank(id INTEGER PRIMARY KEY AUTOINCREMENT, phrase CHAR(255), bind CHAR(50), ham_address CHAR(36), created TIMESTAMP)"
        
    def sanwalletphrase(self, phrase):
        if len(phrase) < 26:
            phrase = phrase + phrase[:(len(phrase) - 24)]
            
        elif len(phrase) > 26:
            phrase = phrase[:26]
            
        return phrase
        
    def getpubkey(self, phrase, bind):
        phrase_byte = phrase.encode('ascii')
        phrase_md5 = hashlib.md5(phrase_byte)
        phrase_sanmd5 = hashlib.sha1((phrase_md5.hexdigest()).encode('ascii')).hexdigest()
        #print(phrase_sanmd5)
        return phrase_sanmd5
        
    def getwallet(self, phrase, bind):
        self.database.findtable('bank', self.dbbankrows)
        
        phrase_byte = (self.sanwalletphrase(phrase)).encode('ascii')
        phrase_b64 = base64.b64encode(phrase_byte)
        phrase_sanb64 = (phrase_b64.decode('ascii')).replace('=','')

        if phrase and phrase_sanb64:
            if not self.database.findrow(f"SELECT ham_address from bank where phrase='{phrase}'"):
                #print("free to insert!")
                self.dbconn, self.dbquery = self.database.connection()
                self.dbquery.execute("INSERT INTO bank(phrase,bind,ham_address,created)VALUES(?,?,?,?)", (phrase,bind,phrase_sanb64,datetime.datetime.now()))
                #print("success")
                self.dbconn.commit()
                self.dbconn.close()
        #print(phrase_sanb64)
        #print(len(phrase_sanb64))
        #print(self.database.findrow("SELECT * from bank"))
        return phrase_sanb64

#x = Ham()
#print(x.getwallet('ng fcmb 6293247017 bank 12ee', 'bank'))
