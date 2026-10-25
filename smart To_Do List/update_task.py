import sqlite3
from datetime import datetime
from recurring import create_next_occurrence


def update_task():
    print("\n" + "=" * 55)
    print("UPDATE TASK".center(55))
    print("=" * 55)

    task_id = input("\nEnter the task ID to update: ").strip()

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
                   is_recurring, recurrence_type, reminder_minutes
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

        (
            title, description, deadline, priority, status,
            is_recurring, recurrence_type, reminder_minutes
        ) = task

        print("\nCurrent Task Details")
        print("-" * 55)
        print(f"1. Title          : {title}")
        print(f"2. Description    : {description}")
        print(f"3. Deadline       : {deadline}")
        print(f"4. Priority       : {priority}")
        print(f"5. Status         : {status}")
        print(f"6. Reminder       : {reminder_minutes} minutes before")
        print("-" * 55)

        choice = input("\nEnter the field number to update (1-6): ").strip()

        fields = {
            "1": ("title", "Enter the new title: "),
            "2": ("description", "Enter the new description: "),
            "3": ("deadline", "Enter the new deadline (YYYY-MM-DD HH:MM): "),
            "4": ("priority", "Enter the new priority (High/Medium/Low): "),
            "5": ("status", "Enter the new status (Pending/Completed): "),
            "6": ("reminder_minutes", "Enter the reminder time in minutes before the deadline: ")
        }

        if choice not in fields:
            print("\nERROR: Invalid choice!")
            return

        column, prompt = fields[choice]
        new_value = input(prompt).strip()

        if column == "title" and not new_value:
            print("\nERROR: Title cannot be empty!")
            return

        if column == "deadline":
            try:
                deadline_dt = datetime.strptime(
                    new_value, "%Y-%m-%d %H:%M"
                )
            except ValueError:
                print("\nERROR: Invalid deadline format!")
                print("Use YYYY-MM-DD HH:MM")
                return

            if deadline_dt <= datetime.now():
                print("\nWARNING: This deadline is in the past!")

                choice = input(
                    "Do you want to continue anyway? (yes/no): "
                ).strip().lower()

                if choice not in ["yes", "no"]:
                    print("Invalid choice! Please enter yes or no.")
                    return

                if choice == "no":
                    print("Deadline update cancelled.")
                    return

            new_value = deadline_dt.strftime("%Y-%m-%d %H:%M:%S")

        if column == "priority":
            new_value = new_value.capitalize()

            if new_value not in ["High", "Medium", "Low"]:
                print("\nERROR: Priority must be High, Medium, or Low!")
                return

        if column == "status":
            new_value = new_value.capitalize()

            if new_value not in ["Pending", "Completed"]:
                print("\nERROR: Status must be Pending or Completed!")
                return

        if column == "reminder_minutes":
            if not new_value.isdigit() or int(new_value) <= 0:
                print("\nERROR: Reminder time must be a positive number of minutes!")
                return

            new_value = int(new_value)

        cursor.execute(
            f"UPDATE tasks SET {column} = ? WHERE task_id = ?",
            (new_value, int(task_id))
        )

        if column in ["deadline", "reminder_minutes"] or (
            column == "status" and new_value == "Pending"
        ):
            cursor.execute(
                """
                UPDATE tasks
                SET reminder_sent = 0
                WHERE task_id = ?
                """,
                (int(task_id),)
            )

        if (
            column == "status"
            and new_value == "Completed"
            and status == "Pending"
            and is_recurring
            and recurrence_type in ["Daily", "Weekly", "Monthly"]
        ):
            create_next_occurrence(cursor, int(task_id))

        conn.commit()

        print("\n" + "=" * 55)
        print("TASK UPDATED SUCCESSFULLY!".center(55))
        print("-" * 55)
        print(f"Task ID      : {task_id}")
        print(f"Updated field: {column}")
        print(f"New value    : {new_value}")
        print("=" * 55)

    except (sqlite3.Error, ValueError) as error:
        conn.rollback()
        print("\n" + "-" * 55)
        print(f"Error: {error}")
        print("-" * 55)

    finally:
        conn.close()


if __name__ == "__main__":
    update_task()