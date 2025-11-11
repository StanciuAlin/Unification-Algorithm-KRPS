from colorama import Fore, Style
from src.models.term import Term
from src.models.errors import InputError
from src.utils.printer import Printer


class InputHandler:
    """Manages user input from the command line for unification tasks."""

    def __init__(self):
        Printer.print_title(" " * 28 +
                            "Unification CLI")
        Printer.print_cli_info()

    @staticmethod
    def _check_parentheses_balance(expr: str):
        """Checks if parentheses in the input expression are balanced."""
        open_count = expr.count("(")
        close_count = expr.count(")")
        if open_count != close_count:
            raise InputError(
                f"Unbalanced parentheses: found {open_count} '(' and {close_count} ')'"
            )

    def read_term(self, prompt: str) -> Term:
        """Reads a term from user input and transforms it into a Term object (AIMA convention)."""
        text = input(prompt).strip()
        if text.lower() == 'e':
            Printer.print_text_color("\n\n  Thank you for using the Unification CLI!",
                                     color="yellow", bold=True, end="\n\n")
            exit(0)

        if not text:
            raise InputError(
                "Empty input is not allowed. Please enter a valid term.")

        # Verify parentheses balance
        self._check_parentheses_balance(text)

        try:
            # Parsing according to AIMA convention:
            # uppercase = variable, lowercase = constant or function
            term = Term.from_string(text)
            # print(Fore.LIGHTBLACK_EX +
            #       f"   → Parsed as: {term}" + Style.RESET_ALL)
            return term
        except Exception as e:
            raise InputError(f"Error while interpreting expression: {e}")
