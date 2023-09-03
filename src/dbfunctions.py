import sqlite3
from sqlite3 import Error

def add_to_db(id, name, rarity, tags, img):
    
    """Add operator in database"""
    
    conn = create_connection("operators.db")
    cur = conn.cursor()
    
    cur.execute("""INSERT INTO operators VALUES(?,?,?,?)""",
                (id, name, rarity, img,))
    
    for tag in tags:
    
        try:
            cur.execute("""INSERT INTO tags(name) VALUES(?)""",
                        (tag,))
        except sqlite3.IntegrityError:
            pass
        else:
            pass
        cur.execute("""SELECT id FROM tags WHERE name = (?)""",
                    (tag,))
        tag_id = cur.fetchone()
        cur.execute("""INSERT INTO operator_tag VALUES(?,?)""",
                    (id, tag_id[0]))
           
    conn.commit()
    conn.close()


def create_tables():
    
    """Create tables if not exists"""
    
    conn = create_connection("operators.db")
    cur = conn.cursor()
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY,
                name TEXT,
                rarity INTEGER,
                img BLOB
                )""")
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS operator_tag (
                operator_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (tag_id)
                    REFERENCES tags (id),    
                FOREIGN KEY (operator_id) 
                    REFERENCES operators (id)
                )""")
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                name TEXT NOT NULL UNIQUE,
                id INTEGER PRIMARY KEY AUTOINCREMENT
                )""")
    
    conn.commit()
    cur.close


def exist_in_db(id):
    
    """Return True if operator in db"""
    
    conn = create_connection("operators.db")
    cur = conn.cursor()
    
    cur.execute("""SELECT * FROM operators WHERE id = ?""", (id,))
    
    if cur.fetchone():
        conn.close
        return True
    
    conn.close()
    
    
def available_tags():
    
    """Returns list of all tags in db"""
    
    conn = create_connection("operators.db")
    cur = conn.cursor()
    
    cur.execute("SELECT name FROM tags")
    tags = cur.fetchall()
    conn.close()
    
    result = []
    for i in range(len(tags)): 
        result.append(tags[i][0])
        
    return result
    

def retrieve_operators_by_tags(tags):
    conn = create_connection("operators.db")
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT operators.name, rarity, tag, img
            FROM 
                (SELECT id, group_concat(name) as tag
                    FROM 
                        (SELECT operators.id, tags.name
                        FROM operators
                        JOIN operator_tag ON operators.id = operator_id
                        JOIN tags ON tags.id = tag_id
                        ORDER BY operators.id, tags.name
                        )
                GROUP BY id
                ) a
            JOIN operators ON a.id = operators.id
            WHERE tag LIKE ?
            ORDER BY rarity DESC
        """, (tags,) 
    )
    
    result = cur.fetchall()
    conn.close()
    return result

    
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn



    