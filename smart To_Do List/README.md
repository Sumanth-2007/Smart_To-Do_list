# Smart To-do List with Automated Email Reminders

## About
A Python-based task management application that uses SQLite to store tasks and SMTP to send email reminders before deadlines.

## Features
- Add, view, update, and delete tasks
- Search and filter tasks
- Set task deadlines and priorities
- Customize email reminder times
- Mark tasks as completed
- Create daily, weekly, and monthly recurring tasks
- Detect overdue tasks
- Validate user inputs

## Technologies Used
- Python
- SQLite
- SMTP
- python-dotenv

## Installation and Execution

1. Extract the project ZIP file and open the folder in VS Code.

2. Install the required dependency:

   ```bash
   pip install -r requirements.txt
   ```

3. To enable email reminders, create a `.env` file in the project folder using `.env.example` as a reference.

4. Enter your email configuration in `.env`:

   ```dotenv
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_gmail_app_password
   RECEIVER_EMAIL=receiver_email@gmail.com
   ```

   For Gmail, use an App Password instead of your regular account password.

5. Run the application:

   ```bash
   python main.py
   ```

## Instructions for the Examiner
- Configure your own email credentials in `.env` to test email reminders.
- Keep the application running for reminder checks.
- The application creates the SQLite database if it does not exist.
- Task management features do not require email credentials, but sending reminders does.

## Security
We should never share the `.env` file because it contains private email credentials.