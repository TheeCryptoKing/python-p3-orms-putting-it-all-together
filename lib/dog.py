import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    # all = []
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed
        # Dog.all.append(self)

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        # saves dog object in databse
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES(?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        #  creates row 
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        # callback function
        dog = cls(
            name=row[1],
            breed=row[2],
            id=row[0]
        )
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        # * = all in sqlite and 
        # fetchall = fetches all (or all remaining) rows of a query result set and returns a list of tuples
        return [cls.new_from_db(row) for row in CURSOR.execute(sql).fetchall()]
    

    @classmethod
    def find_by_name(cls,name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        # ? placholder for data passesed in 
        row = CURSOR.execute(sql, (name,)).fetchone()
        # fetchone = retrieves the next row of a query result set and returns a single sequence, or None if no more rows are available
        if not row:
            return None
        
        return Dog( 
            name=row[1], 
            breed=row[2], 
            id=row[0]
        )
    

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ? 
            LIMIT 1
        """
        
        row = CURSOR.execute(sql, (id,)).fetchone()
        if not row:
            return None
        
        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )
    
    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
            """
          

        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
                  
            CURSOR.execute(sql, (name, breed))   
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid
            )

        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

