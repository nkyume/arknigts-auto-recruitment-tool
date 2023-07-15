from PIL import Image
import io
import sqlite3

conn = sqlite3.connect("operators.db")
cur = conn.cursor()

cur.execute("""SELECT name, rarity, img FROM operators WHERE name = 'Melantha'""")

name, rarity, img_data = cur.fetchone()

file = io.BytesIO(img_data)
img = Image.open(file)
img.show()
print(name, rarity)


