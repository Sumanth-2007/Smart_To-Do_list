import sqlite3

def delete_task():
    print("\n" + "=" * 55)
    print("DELETE TASK".center(55))
    print("=" * 55)

    task_id = input("\nEnter the task ID to delete: ").strip()

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
            SELECT task_id, title, description, deadline, priority, status
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

        print("\n" + "-" * 55)
        print("TASK DETAILS".center(55))
        print("-" * 55)
        print(f"Task ID     : {task[0]}")
        print(f"Title       : {task[1]}")
        print(f"Description : {task[2] or 'None'}")
        print(f"Deadline    : {task[3]}")
        print(f"Priority    : {task[4]}")
        print(f"Status      : {task[5]}")
        print("-" * 55)

        confirm = input(
            "\nAre you sure you want to delete this task? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("\nTask deletion cancelled.")
            return

        cursor.execute(
            "DELETE FROM tasks WHERE task_id = ?",
            (int(task_id),)
        )

        conn.commit()

        print("\n" + "=" * 55)
        print("TASK DELETED SUCCESSFULLY!".center(55))
        print("=" * 55)

    except sqlite3.Error as error:
        print(f"\nDatabase error: {error}")

    finally:
        conn.close()

if __name__ == "__main__":
    delete_task()