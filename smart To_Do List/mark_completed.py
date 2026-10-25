import sqlite3
from recurring import create_next_occurrence


def mark_completed():
    print("\n" + "=" * 55)
    print("MARK TASK AS COMPLETED".center(55))
    print("=" * 55)

    task_id = input("\nEnter the task ID: ").strip()

    if not task_id.isdigit() or int(task_id) == 0:
        print("\n" + "-" * 55)
        print("ERROR: Please enter a valid task ID!")
        print("-" * 55)
        return

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT title, description, deadline, priority, status,
                   is_recurring, recurrence_type
            FROM tasks
            WHERE task_id = ?
            """,
            (int(task_id),)
        )

        task = cursor.fetchone()

        if task is None:
            print("\n" + "-" * 55)
            print("ERROR: Task not found!")
            print("-" * 55)
            return

        title, description, deadline, priority, status, is_recurring, recurrence_type = task

        if status == "Completed":
            print("\n" + "-" * 55)
            print("This task is already completed!")
            print("-" * 55)
            return

        cursor.execute(
            """
            UPDATE tasks
            SET status = 'Completed'
            WHERE task_id = ?
            """,
            (int(task_id),)
        )

        print("\n" + "=" * 55)
        print("TASK COMPLETED SUCCESSFULLY!".center(55))
        print("-" * 55)
        print(f"Task ID : {task_id}")
        print(f"Title   : {title}")
        print("Status  : Completed")

        if is_recurring and recurrence_type in ["Daily", "Weekly", "Monthly"]:
            create_next_occurrence(cursor, int(task_id))

        conn.commit()
        print("=" * 55)

    except (sqlite3.Error, ValueError) as error:
        conn.rollback()
        print("\n" + "-" * 55)
        print(f"Error: {error}")
        print("-" * 55)

    finally:
        conn.close()


if __name__ == "__main__":
    mark_completed()