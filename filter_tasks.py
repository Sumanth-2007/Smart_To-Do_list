import sqlite3


def filter_tasks():
    print("\n" + "=" * 55)
    print("|" + "FILTER TASKS".center(53) + "|")
    print("=" * 55)

    print("|" + "  1. Filter by Status".ljust(53) + "|")
    print("|" + "  2. Filter by Priority".ljust(53) + "|")
    print("|" + "  3. Back".ljust(53) + "|")

    print("=" * 55)

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "3":
        return

    if choice == "1":
        column = "status"
        allowed_values = ["Pending", "Completed"]
        print("\nAvailable statuses: Pending, Completed")
        value = input("Enter status: ").strip().capitalize()

    elif choice == "2":
        column = "priority"
        allowed_values = ["High", "Medium", "Low"]
        print("\nAvailable priorities: High, Medium, Low")
        value = input("Enter priority: ").strip().capitalize()

    else:
        print("\nInvalid choice!")
        return

    if value not in allowed_values:
        print("\nInvalid value entered!")
        return

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    try:
        query = f"""
            SELECT task_id, title, description, deadline, priority, status
            FROM tasks
            WHERE {column} = ?
            ORDER BY task_id
        """

        cursor.execute(query, (value,))
        tasks = cursor.fetchall()

        print("\n" + "=" * 120)
        print(f"TASKS FILTERED BY {column.upper()}".center(120))
        print("=" * 120)

        if not tasks:
            print("No matching tasks found.".center(120))
        else:
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
    filter_tasks()