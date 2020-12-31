from peewee import SqliteDatabase, TextField, DateTimeField, Model
from datetime import datetime

db = SqliteDatabase('puzzles.db')

class Puzzle(Model):
    name = TextField(unique=True)
    channel = TextField(unique=True)
    channel_id = TextField(unique=True)
    sheet = TextField()

    creator = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

if __name__ == '__main__':
    db.create_tables([Puzzle])
