"""Small SQLite helper used by app.py (same idea as the dbhelper shown in the tutorial video)."""
import os
import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = os.environ.get(
    "SCHOOL_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "school.db")
)


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def getprocess(sql: str, vals: tuple = ()) -> list:
    conn = connect()
    try:
        cur = conn.execute(sql, vals)
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print("Error:", e)
        return []
    finally:
        conn.close()


def postprocess(sql: str, vals: tuple = ()) -> bool:
    conn = connect()
    try:
        cur = conn.execute(sql, vals)
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.Error as e:
        print("Error:", e)
        return False
    finally:
        conn.close()


def getall(table: str) -> list:
    return getprocess(f"SELECT * FROM `{table}`")


def getrecord(table: str, **kwargs) -> list:
    keys = list(kwargs.keys())
    vals = tuple(kwargs.values())
    where = " AND ".join(f"`{k}`=?" for k in keys)
    return getprocess(f"SELECT * FROM `{table}` WHERE {where}", vals)


def addrecord(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    vals = tuple(kwargs.values())
    cols = ",".join(f"`{k}`" for k in keys)
    marks = ",".join("?" for _ in keys)
    return postprocess(f"INSERT INTO `{table}`({cols}) VALUES({marks})", vals)


def deleterecord(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    vals = tuple(kwargs.values())
    where = " AND ".join(f"`{k}`=?" for k in keys)
    return postprocess(f"DELETE FROM `{table}` WHERE {where}", vals)


def init_db() -> None:
    """Create the tables (and sample rows) the first time the app runs."""
    conn = connect()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS students(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               idno VARCHAR(20),
               lastname VARCHAR(50),
               firstname VARCHAR(50),
               course VARCHAR(20),
               level INTEGER)"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email VARCHAR(50) UNIQUE,
               password VARCHAR(255),
               name VARCHAR(50))"""
    )
    if conn.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO students(idno,lastname,firstname,course,level) VALUES(?,?,?,?,?)",
            [
                ("1000", "hello", "world", "bsit", 2),
                ("1001", "alpha", "zulu", "bsit", 3),
                ("1002", "bravo", "yankee", "bsit", 2),
                ("1003", "charlie", "xray", "bsit", 1),
                ("1004", "delta", "whiskey", "bscs", 2),
                ("1005", "echo", "victor", "bscs", 3),
            ],
        )
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO users(email,password,name) VALUES(?,?,?)",
            ("alpha@uc.com", generate_password_hash("hello123"), "alpha"),
        )
    conn.commit()
    conn.close()
