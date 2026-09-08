from agent import ask_ai, propose_calendar_event
from calendar_tool import create_calendar_event
from tools import clear_all_tasks


def confirm(prompt="Do you want to continue? (yes/no): "):
    return input(prompt).strip().lower() == "yes"


def handle_calendar_request(user_input):
    proposal = propose_calendar_event(user_input)

    if proposal["status"] == "not_calendar":
        return False

    if proposal["status"] in {"error", "missing_details"}:
        print(f"\nAssistant: {proposal['message']}\n")
        return True

    print("\nAssistant: Proposed Google Calendar action")
    print(f"Title: {proposal['summary']}")
    print(f"Start: {proposal['start_datetime']}")
    print(f"End: {proposal['end_datetime']}")
    print(f"Timezone: {proposal['timezone_name']}")
    print("\nThis will create a real event in your Google Calendar.")

    if not confirm("Create this event? (yes/no): "):
        print("\nAssistant: Action cancelled.\n")
        return True

    result = create_calendar_event(
        summary=proposal["summary"],
        start_datetime=proposal["start_datetime"],
        end_datetime=proposal["end_datetime"],
        timezone_name=proposal["timezone_name"],
    )

    print("\nAssistant:")
    if result["status"] == "success":
        print("Calendar event created successfully.")
        print(result["html_link"])
    else:
        print(result["message"])
    print()
    return True


def main():
    print("=" * 50)
    print("AI Executive Assistant Agent")
    print("=" * 50)
    print("Type 'exit' to close the assistant.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\nAssistant: Goodbye!")
            break

        if user_input.lower() in {
            "delete all tasks",
            "clear all tasks",
            "remove all tasks",
        }:
            print("\nAssistant: This action will permanently delete all saved tasks.")

            if confirm():
                result = clear_all_tasks()
                print(f"\nAssistant: {result['message']}\n")
            else:
                print("\nAssistant: Action cancelled.\n")
            continue

        calendar_keywords = (
            "calendar",
            "schedule",
            "meeting",
            "appointment",
            "event",
            "موعد",
            "اجتماع",
            "التقويم",
        )

        if any(keyword in user_input.lower() for keyword in calendar_keywords):
            if handle_calendar_request(user_input):
                continue

        response = ask_ai(user_input)
        print(f"\nAssistant:\n{response}\n")


if __name__ == "__main__":
    main()
