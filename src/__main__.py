import sys

from ui.cli import start_cli
from ui.gui import start_gui

def launch():
    """
    Launches the application, allowing the user to choose between CLI and GUI modes.
    Returns: None
    """
    try:
        print("\n1) Run CLI\n2) Run GUI")
        choice = input(">> Enter your choice: ")
        if choice == '1':
            start_cli()

        elif choice == '2':
            start_gui()
            sys.exit(0)

        else:
            print("\n>> [ERROR] Invalid choice. Please enter 1 or 2.\n")

        m = input("\n>> Program closed. Return to main menu? (y/n): ")
        if m.lower() == 'y':
            return False
        return True


    except KeyboardInterrupt:
        print("\n\nExiting program...\n")
        sys.exit(0)

    except Exception as e:
        print(f"[ERROR] -> {e}")
        return False


if __name__ == "__main__":
    print("\nPress Ctrl+C to exit at any time")
    run = True
    while run:
        run = launch()
    print("\n>> [INFO] Exiting...")

