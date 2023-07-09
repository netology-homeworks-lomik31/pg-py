import psycopg2 as pg, pprint

class DB:
    def __createTables(self):
        with self.__conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS user_ (id SERIAL PRIMARY KEY, first_name VARCHAR(30) NOT NULL, last_name VARCHAR(30) NOT NULL, email VARCHAR(50) NOT NULL UNIQUE );")
            cur.execute("CREATE TABLE IF NOT EXISTS user_phones (user_id INT NOT NULL REFERENCES user_(id), phone BIGINT UNIQUE, PRIMARY KEY (user_id, phone));")
            self.__conn.commit()
        
    def __init__(self, host, dbname, user, password) -> None:
        self.__conn = pg.connect(host = host, dbname = dbname, user = user, password = password)
        self.__createTables()

    def newUser(self, firstName: str, lastName: str, email: str, phones: tuple = (None,)):
        with self.__conn.cursor() as cur:
            cur.execute("INSERT INTO user_(first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id", (firstName, lastName, email))
            if not (phones[0] is None): self.addUserPhone(cur.fetchone(), phones)
            else: self.__conn.commit()

    def addUserPhone(self, userId: int, phones: tuple):
        with self.__conn.cursor() as cur:
            for i in phones:
                if (isinstance(i, int)): cur.execute("INSERT INTO user_phones(user_id, phone) VALUES (%s, %s)", (userId, i))
            self.__conn.commit()
    
    def editUser(self, userId: int, firstName: str = None, lastName: str = None, email: str = None, phone: tuple = None): # телефон -> (старый телефон, новый телефон)
        with self.__conn.cursor() as cur:
            if (firstName): cur.execute("UPDATE user_ SET first_name = %s WHERE id = %s", (firstName, userId))
            if (lastName): cur.execute("UPDATE user_ SET last_name = %s WHERE id = %s", (lastName, userId))
            if (email): cur.execute("UPDATE user_ SET email = %s WHERE id = %s", (email, userId))
            if (phone): cur.execute("UPDATE user_phones SET phone = %s WHERE phone = %s AND user_id = %s", (*phone[::-1], userId))
            self.__conn.commit()
    
    def delPhone(self, userId, phone):
        with self.__conn.cursor() as cur:
            cur.execute("DELETE FROM user_phones WHERE user_id = %s AND phone = %s", (userId, phone))
            self.__conn.commit()
    
    def delUser(self, userId):
        with self.__conn.cursor() as cur:
            cur.execute("DELETE FROM user_phones WHERE user_id = %s", (userId,))
            cur.execute("DELETE FROM user_ WHERE id = %s", (userId,))
            self.__conn.commit()
    
    def searchUser(self, firstName = None, lastName = None, email = None, phone = None):
        with self.__conn.cursor() as cur:
            if (firstName): cur.execute("SELECT id, first_name FROM user_ WHERE first_name = %s", (firstName,))
            elif (lastName): cur.execute("SELECT id, last_name FROM user_ WHERE last_name = %s", (lastName,))
            elif (email): cur.execute("SELECT id, email FROM user_ WHERE email = %s", (email,))
            elif (phone): cur.execute("SELECT id, phone FROM user_ JOIN user_phones ON user_id = id WHERE phone = %s", (phone,))
            return cur.fetchall()


    def close(self):
        self.__conn.close()

# with pg.connect(
#     host = "lomik31.codead.dev",
#     dbname = "netology_hw_1",
#     user = "lomik31",
#     password = "neptun2004"
# ) as conn:
#     with conn.cursor() as cur:
#         cur.execute("SELECT track.id, track.name, artist.name FROM track JOIN album ON track.album = album.id JOIN album_artist ON album_artist.album = album.id JOIN artist ON album_artist.artist = artist.id ORDER BY track.id")
#         pprint.pprint(cur.fetchall())