import os
import psycopg
from psycopg.rows import dict_row

class Repository:
    def connect(self): return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)
    def initialize(self):
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT FALSE)")
            db.execute("CREATE TABLE IF NOT EXISTS initialization (id INTEGER PRIMARY KEY)")
            db.execute("LOCK TABLE initialization IN EXCLUSIVE MODE")
            if not db.execute("SELECT id FROM initialization WHERE id = 1").fetchone():
                if not db.execute("SELECT 1 FROM tasks LIMIT 1").fetchone():
                    db.execute("INSERT INTO tasks (title) VALUES (%s), (%s), (%s)",
                               ("Learn APIs", "Read a book", "Take a walk"))
                db.execute("INSERT INTO initialization (id) VALUES (1)")
    def list(self):
        with self.connect() as db: return db.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    def get(self, task_id):
        with self.connect() as db: return db.execute("SELECT * FROM tasks WHERE id = %s", (task_id,)).fetchone()
    def create(self, title):
        with self.connect() as db: return db.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING *", (title,)).fetchone()
    def update(self, task_id, changes):
        with self.connect() as db:
            old = db.execute("SELECT * FROM tasks WHERE id = %s FOR UPDATE", (task_id,)).fetchone()
            if not old: return None
            old.update(changes); return db.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *", (old["title"], old["done"], task_id)).fetchone()
    def delete(self, task_id):
        with self.connect() as db: return db.execute("DELETE FROM tasks WHERE id = %s", (task_id,)).rowcount > 0
