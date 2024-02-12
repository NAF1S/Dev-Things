import sqlite3

if __name__ == "__main__":
    db = sqlite3.connect("store.db")

    with open ("database.sql", "r") as d:
        db.executescript(d.read())
    
    db.commit()
    db.close()