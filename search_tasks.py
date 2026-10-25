import sqlite3

def search_tasks():
    keyword = input("\nEnter a title or keyword to search: ").strip()

    if not keyword:
        print("\nSearch keyword cannot be empty!")
        return

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    try:
        query = """
            SELECT task_id, title, description, deadline, priority, status
            FROM tasks
            WHERE title LIKE ?
            ORDER BY task_id
        """

        cursor.execute(query, (f"%{keyword}%",))
        tasks = cursor.fetchall()

        print("\n" + "=" * 120)
        print("SEARCH RESULTS".center(120))
        print("=" * 120)

        if not tasks:
            print("No matching tasks found.".center(120))
            return

        print(
            f"{'ID':<6}"
            f"{'TITLE':<30}"
            f"{'DESCRIPTION':<35}"
            f"{'DEADLINE':<24}"
            f"{'PRIORITY':<15}"
            f"{'STATUS':<12}"
        )

        print("-" * 120)

        for task in tasks:
            task_id, title, description, deadline, priority, status = task

            print(
                f"{task_id:<6}"
                f"{title:<30}"
                f"{description:<35}"
                f"{deadline:<24}"
                f"{priority:<15}"
                f"{status:<12}"
            )

        print("-" * 120)
        print(f"Total matching tasks: {len(tasks)}".center(120))
        print("=" * 120)

    except sqlite3.Error as error:
        print(f"\nDatabase error: {error}")

    finally:
        conn.close()


if __name__ == "__main__":
    search_tasks()