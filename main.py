from agent import ask_ai
from tools import clear_all_tasks


def main():
    print("=" * 50)
    print("AI Executive Assistant Agent")
    print("=" * 50)
    print("Type 'exit' to close the assistant.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("\nAssistant: Goodbye!")
            break

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
                print(
                    "\nAssistant: Action cancelled."
                )

            print()
            continue

        response = ask_ai(user_input)

        print("\nAssistant:")
        print(response)
        print()


if __name__ == "__main__":
    main()