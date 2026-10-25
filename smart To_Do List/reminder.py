import smtplib
from email.message import EmailMessage
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_email(receiver_email, subject, body):
    message = EmailMessage()

    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject

    message.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        print("Email sent successfully!")
        return True

    except Exception as error:
        print(f"Failed to send email: {error}")
        return False

def get_pending_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT task_id, title, deadline, reminder_minutes
        FROM tasks
        WHERE status = 'Pending'
        AND reminder_sent = 0
    """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks

def mark_reminder_sent(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET reminder_sent = 1 WHERE task_id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

def check_reminders():
    tasks = get_pending_tasks()

    current_time = datetime.now()

    for task in tasks:
        task_id, title, deadline, reminder_minutes = task

        deadline_time = datetime.strptime(
            deadline, "%Y-%m-%d %H:%M:%S"
        )

        reminder_time = deadline_time - timedelta(
            minutes=reminder_minutes
        )

        if reminder_time <= current_time <= deadline_time:
            subject = f"🚨 DEADLINE ALERT: {title}!"

            body = (
                "⚠️ Hey! Time is running out!\n\n"
                f"📌 Task: {title}\n"
                f"🕒 Deadline: {deadline}\n\n"
                "Don't wait until the last minute! 🔥\n"
                "Get it done before the deadline!"
            )

            email_sent = send_email(
                RECEIVER_EMAIL,
                subject,
                body
            )

            if email_sent:
                mark_reminder_sent(task_id)
                print(f"Reminder email sent for task: {title}")

if __name__ == "__main__":
    send_email(
        RECEIVER_EMAIL,
        "Test Email - Smart To-Do List",
        "Hello! This is a test email from your Smart To-Do List application."
    )