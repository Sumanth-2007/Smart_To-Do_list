import sqlite3
from datetime import datetime


def add_task():
    print("\n" + "=" * 55)
    print("ADD NEW TASK".center(55))
    print("=" * 55)

    title = input("\nEnter task title: ").strip()

    if not title:
        print("\n" + "-" * 55)
        print("ERROR: Task title cannot be empty!")
        print("-" * 55)
        return

    description = input("Enter description (optional): ").strip()

    deadline = input("Enter deadline (YYYY-MM-DD HH:MM): ").strip()

    try:
        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        print("\n" + "-" * 55)
        print("ERROR: Invalid deadline!")
        print("Expected format: YYYY-MM-DD HH:MM")
        print("-" * 55)
        return

    if deadline_dt <= datetime.now():
        print("\n" + "-" * 55)
        print("WARNING: This deadline is in the past!")
        print("-" * 55)

        choice = input(
            "Do you want to continue anyway? (yes/no): "
        ).strip().lower()

        if choice not in ["yes", "no"]:
            print("Invalid choice! Please enter yes or no.")
            return

        if choice == "no":
            print("Task creation cancelled.")
            return

    priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()

    if priority not in ["High", "Medium", "Low"]:
        print("\n" + "-" * 55)
        print("ERROR: Invalid priority!")
        print("Choose High, Medium, or Low.")
        print("-" * 55)
        return

    status = input("Enter status (Pending/Completed): ").strip().capitalize()

    if status not in ["Pending", "Completed"]:
        print("\n" + "-" * 55)
        print("ERROR: Invalid status!")
        print("Choose Pending or Completed.")
        print("-" * 55)
        return

    reminder_input = input(
        "Enter reminder time in minutes before the deadline: "
    ).strip()

    if not reminder_input.isdigit() or int(reminder_input) <= 0:
        print("\n" + "-" * 55)
        print("ERROR: Reminder time must be a positive number!")
        print("-" * 55)
        return

    reminder_minutes = int(reminder_input)

    recurring = input("Is this a recurring task? (yes/no): ").strip().lower()

    if recurring not in ["yes", "no"]:
        print("Invalid choice! Enter yes or no.")
        return

    is_recurring = 1 if recurring == "yes" else 0

    recurrence_type = None

    if is_recurring:
        recurrence_type = input(
            "Repeat how often? (Daily/Weekly/Monthly): "
        ).strip().capitalize()

        if recurrence_type not in ["Daily", "Weekly", "Monthly"]:
            print("Invalid recurrence type!")
            print("Choose Daily, Weekly, or Monthly.")
            return

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    query = """
        INSERT INTO tasks (
            title,
            description,
            created_at,
            deadline,
            priority,
            status,
            reminder_minutes,
            reminder_sent,
            is_recurring,
            recurrence_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = (
        title,
        description,
        created_at,
        deadline_dt.strftime("%Y-%m-%d %H:%M:%S"),
        priority,
        status,
        reminder_minutes,
        0,
        is_recurring,
        recurrence_type
    )

    try:
        cursor.execute(query, values)
        task_id = cursor.lastrowid
        conn.commit()

        print("\n" + "=" * 55)
        print("TASK ADDED SUCCESSFULLY!".center(55))
        print("-" * 55)
        print(f"Task ID          : {task_id}")
        print(f"Created At       : {created_at}")
        print(f"Reminder         : {reminder_minutes} minutes before")
        print("=" * 55)

    except sqlite3.Error as error:
        conn.rollback()
        print("\n" + "-" * 55)
        print(f"Database error: {error}")
        print("-" * 55)

    finally:
        conn.close()


if __name__ == "__main__":
    add_task()