import sqlite3
from dataclasses import dataclass


@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
    favorite: int = 0


class Database:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename + '.db')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY,
                                                 title TEXT,
                                                 content TEXT NOT NULL,
                                                 favorite INTEGER NOT NULL DEFAULT 0 );'''
        )

    def add(self, note):
        self.conn.execute(
            'INSERT INTO note (title, content, favorite) VALUES (?, ?, ?);',
            (note.title, note.content, note.favorite)
        )
        self.conn.commit()

    def get_all(self):
        # As anotações favoritas aparecem primeiro na listagem
        cursor = self.conn.execute(
            'SELECT id, title, content, favorite FROM note ORDER BY favorite DESC, id;'
        )

        notes = []
        for linha in cursor:
            notes.append(Note(id=linha[0], title=linha[1],
                              content=linha[2], favorite=linha[3]))

        return notes

    def get(self, note_id):
        cursor = self.conn.execute(
            'SELECT id, title, content, favorite FROM note WHERE id = ?;',
            (note_id,)
        )

        linha = cursor.fetchone()
        if linha is None:
            return None

        return Note(id=linha[0], title=linha[1],
                    content=linha[2], favorite=linha[3])

    def update(self, note):
        self.conn.execute(
            'UPDATE note SET title = ?, content = ?, favorite = ? WHERE id = ?;',
            (note.title, note.content, note.favorite, note.id)
        )
        self.conn.commit()

    def delete(self, note_id):
        self.conn.execute('DELETE FROM note WHERE id = ?;', (note_id,))
        self.conn.commit()
