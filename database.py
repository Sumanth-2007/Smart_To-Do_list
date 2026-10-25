import sqlite3

def create_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            deadline TEXT NOT NULL,
            priority TEXT NOT NULL
                CHECK (priority IN ('High', 'Medium', 'Low')),
            status TEXT NOT NULL DEFAULT 'Pending'
                CHECK (status IN ('Pending', 'Completed')),
            reminder_minutes INTEGER DEFAULT 15,
            reminder_sent INTEGER DEFAULT 0,
            is_recurring INTEGER DEFAULT 0,
            recurrence_type TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database and tasks table created successfully!")

if __name__ == "__main__":
    create_database()