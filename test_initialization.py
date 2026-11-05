from repository import Repository


def test_clean_database_seeds_three_tasks_once_across_restarts():
    repo = Repository()
    repo.initialize()
    original = repo.list()
    assert [row['title'] for row in original] == ['Learn APIs', 'Read a book', 'Take a walk']
    assert all(row['done'] is False for row in original)
    for _ in range(3):
        reopened = Repository()
        reopened.initialize()
        assert reopened.list() == original


def test_existing_task_table_is_not_seeded():
    repo = Repository()
    with repo.connect() as db:
        db.execute('CREATE TABLE tasks (id SERIAL PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT FALSE)')
        db.execute('INSERT INTO tasks (title) VALUES (%s)', ('Already here',))
    repo.initialize()
    assert [row['title'] for row in repo.list()] == ['Already here']


def test_intentional_deletion_does_not_reintroduce_examples():
    repo = Repository()
    repo.initialize()
    assert len(repo.list()) == 3
    for row in repo.list():
        repo.delete(row['id'])
    repo.initialize()
    assert repo.list() == []
