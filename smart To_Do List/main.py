from database import create_database
from add_task import add_task
from view_tasks import view_tasks
from update_task import update_task
from delete_task import delete_task
from mark_completed import mark_completed
from search_tasks import search_tasks
from filter_tasks import filter_tasks
from reminder import check_reminders
from overdue_tasks import view_overdue_tasks


def main():
    create_database()

    while True:

        check_reminders()
        
        print("\n" + "=" * 55)
        print("|" + "SMART TO-DO LIST".center(53) + "|")
        print("=" * 55)

        print("|" + " " * 53 + "|")
        print("|" + "  1. Add Task".ljust(53) + "|")
        print("|" + "  2. View Tasks".ljust(53) + "|")
        print("|" + "  3. Update Task".ljust(53) + "|")
        print("|" + "  4. Delete Task".ljust(53) + "|")
        print("|" + "  5. Mark Task as Completed".ljust(53) + "|")
        print("|" + "  6. Search Tasks".ljust(53) + "|")
        print("|" + "  7. Filter Tasks".ljust(53) + "|")
        print("|" + "  8. View overdue tasks".ljust(53) + "|")
        print("|" + "  9. Exit".ljust(53) + "|")
        print("|" + " " * 53 + "|")

        print("=" * 55)

        choice = input("  Enter your choice (1-9): ").strip()

        print("=" * 55)

        if choice == "1":
            add_task()

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            update_task()

        elif choice == "4":
            delete_task()

        elif choice == "5":
            mark_completed()

        elif choice == "6":
            search_tasks()

        elif choice == "7":
            filter_tasks()

        elif choice == "8":
            view_overdue_tasks()

        elif choice == "9":
            print("\n" + "=" * 55)
            print("THANK YOU FOR USING SMART TO-DO LIST!".center(55))
            print("=" * 55)
            break

        else:
            print("\n" + "-" * 55)
            print("Invalid choice! Please enter a number from 1 to 8.")
            print("-" * 55)

        input("\nPress enter to return to the main menu...")    


if __name__ == "__main__":
    main()