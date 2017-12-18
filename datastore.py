import sqlite3

CREATE_DB_QUERY = """CREATE TABLE IF NOT EXISTS links (
                        Type text NOT NULL,
                        RedditId text PRIMARY KEY
                        )
"""


def connect_datastore():
    conn = sqlite3.connect('links.db')
    conn.execute(CREATE_DB_QUERY)
    conn.row_factory = sqlite3.Row
    return conn


def insert_link(db, reddit_id):
    if 't3_' in reddit_id:
        type_text = 'Submission'
    else:
        type_text = 'Comment'

    query = f"INSERT INTO links (Type, RedditId) VALUES('{type_text}', '{reddit_id}')"
    db.execute(query)
    db.commit()


def get_all_links(db):
    query = "SELECT * FROM links"
    results = db.execute(query)
    return results.fetchall()


def clear_datastore(db):
    db.execute('DELETE FROM links')
