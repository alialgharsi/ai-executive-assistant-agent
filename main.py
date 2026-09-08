from agent import ask_ai
from tools import clear_all_tasks
from calendar_tool import create_calendar_event


def main():
    print("=" * 50)
    print("AI Executive Assistant Agent")
    print("=" * 50)
    print("Type 'exit' to close the assistant.\n")

    while True:
        user_input = input("You: ")

        # Exit
        if user_input.lower() == "exit":
            print("\nAssistant: Goodbye!")
            break

        # Sensitive action: Delete all tasks
        if user_input.lower() in [
            "delete all tasks",
            "clear all tasks",
            "remove all tasks"
        ]:
            print(
                "\nAssistant: This action will permanently "
                "delete all saved tasks."
            )

            approval = input(
                "Do you want to continue? (yes/no): "
            )

            if approval.lower() == "yes":
                result = clear_all_tasks()

                print("\nAssistant:")
                print(result["message"])

            else:
                print("\nAssistant: Action cancelled.")

            print()
            continue

        # Sensitive action: Create Google Calendar event
        if user_input.lower() == "create test calendar event":
            print(
                "\nAssistant: This action will create "
                "a real event in your Google Calendar."
            )

            approval = input(
                "Do you want to continue? (yes/no): "
            )

            if approval.lower() == "yes":
                result = create_calendar_event(
                    summary="AI Agent Test Event",
                    start_datetime="2026-09-08T18:00:00",
                    end_datetime="2026-09-08T19:00:00",
                    timezone_name="Asia/Riyadh"
                )

                print("\nAssistant:")

                if result["status"] == "success":
                    print("Calendar event created successfully.")
                    print(result["html_link"])
                else:
                    print(result["message"])
            else:
                print("\nAssistant: Action cancelled.")

            print()
            continue

        # Normal AI conversation
        response = ask_ai(user_input)

        print("\nAssistant:")
        print(response)
        print()


if __name__ == "__main__":
    main()