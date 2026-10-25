import sqlite3

def view_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    print("\n" + "=" * 55)
    print("|" + "VIEW TASKS".center(53) + "|")
    print("=" * 55)

    print("|" + " "*53 + "|")
    print("|" + "  Choose how to display your tasks:".ljust(53) + "|")
    print("|" + " "*53 + "|")

    print("|" + "  1. Default order (Task ID)".ljust(53) + "|")
    print("|" + "  2. Sort by deadline".ljust(53) + "|")
    print("|" + "  3. Sort by priority".ljust(53) + "|")

    print("=" * 55)

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        order = "task_id"
    elif choice == "2":
        order = "deadline"
    elif choice == "3":
        order = """
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
            END
        """
    else:
        print("Invalid choice! Displaying tasks in default order.")
        order = "task_id"

    query = f"""
        SELECT task_id, title, description, deadline, priority, status
        FROM tasks
        ORDER BY {order}
    """

    cursor.execute(query)
    tasks = cursor.fetchall()

    conn.close()

    if not tasks:
        print("No tasks found!")
        return

    print("\n" + "=" * 120)
    print("YOUR TASKS".center(120))
    print("=" * 120)

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
    print(f"Total tasks: {len(tasks)}".center(120))
    print("=" * 120)

if __name__ == "__main__":
    view_tasks()