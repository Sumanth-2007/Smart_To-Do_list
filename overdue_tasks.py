import sqlite3
from datetime import datetime


def view_overdue_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        SELECT task_id, title, description, deadline, priority
        FROM tasks
        WHERE status = 'Pending'
        AND deadline < ?
        ORDER BY deadline ASC
        """,
        (current_time,)
    )

    tasks = cursor.fetchall()
    conn.close()

    print("\n" + "=" * 65)
    print("OVERDUE TASKS".center(65))
    print("=" * 65)

    if not tasks:
        print("\nNo overdue tasks found!")
        print("=" * 65)
        return

    for task in tasks:
        task_id, title, description, deadline, priority = task

        print(f"\nTask ID     : {task_id}")
        print(f"Title       : {title}")
        print(f"Description : {description or 'N/A'}")
        print(f"Deadline    : {deadline}")
        print(f"Priority    : {priority}")
        print("Status      : OVERDUE")
        print("-" * 65)

    print(f"Total overdue tasks: {len(tasks)}")
    print("=" * 65)


if __name__ == "__main__":
    view_overdue_tasks()