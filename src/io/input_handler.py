from src.models.term import Term
from src.models.errors import InputError
from src.utils.printer import print_title


class InputHandler:
    """Manages user input from the command line for unification tasks."""

    def __init__(self):
        print_title(" " * 30 + "🧩 Unification CLI")
        print("ℹ️ Write two logical propostions like King(x), King(John), to unify them.")
        print("  Write 'e' or 'E' to leave the execution.\n")

    def read_term(self, prompt: str) -> Term:
        """Read a term from user input and transform it into a Term object."""
        text = input(prompt).strip()
        if text.lower() in ['e', 'E']:  # ["exit", "quit", "stop"]:
            print("Thank you! 👋")
            exit(0)

        if not text:
            raise InputError(
                "Emty input is not allowed. Please enter a valid term.")

        try:
            term = Term.from_string(text)
            return term
        except Exception as e:
            raise InputError(f"Error at expression interpreting: {e}")
