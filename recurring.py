import sqlite3
from datetime import datetime, timedelta
import calendar


def create_next_occurrence(cursor, task_id):
    cursor.execute("""
        SELECT title, description, deadline, priority,
               reminder_minutes, is_recurring, recurrence_type
        FROM tasks
        WHERE task_id = ?
    """, (task_id,))

    task = cursor.fetchone()

    if task is None:
        return

    title, description, deadline, priority, reminder_minutes, is_recurring, recurrence_type = task

    if not is_recurring or recurrence_type not in ["Daily", "Weekly", "Monthly"]:
        return

    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")

    if recurrence_type == "Daily":
        next_deadline = deadline_dt + timedelta(days=1)

    elif recurrence_type == "Weekly":
        next_deadline = deadline_dt + timedelta(weeks=1)

    else:
        year = deadline_dt.year
        month = deadline_dt.month + 1

        if month > 12:
            month = 1
            year += 1

        day = min(
            deadline_dt.day,
            calendar.monthrange(year, month)[1]
        )

        next_deadline = deadline_dt.replace(
            year=year, month=month, day=day
        )

    next_deadline_str = next_deadline.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        SELECT task_id FROM tasks
        WHERE title = ? AND deadline = ?
          AND is_recurring = 1 AND recurrence_type = ?
    """, (title, next_deadline_str, recurrence_type))

    if cursor.fetchone():
        print("The next recurring task already exists!")
        return

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO tasks (
            title, description, created_at, deadline,
            priority, status, reminder_minutes,
            reminder_sent, is_recurring, recurrence_type
        )
        VALUES (?, ?, ?, ?, ?, 'Pending', ?, 0, ?, ?)
    """, (
        title, description, created_at, next_deadline_str,
        priority, reminder_minutes, is_recurring, recurrence_type
    ))

    print("-" * 55)
    print("NEXT RECURRING TASK CREATED!")
    print("New Task ID:", cursor.lastrowid)
    print("Next Deadline:", next_deadline_str)
    print("Repeat:", recurrence_type)
    print("-" * 55)