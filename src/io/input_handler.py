from src.logic.parser import ParserAIMA
from src.models.errors import InputError
from src.models.term import Term
from src.utils.printer import Printer
from tests.test_unification import run_all_tests


class InputHandler:
    """Console-facing orchestrator that validates, parses, and routes user expressions to the unifier CLI."""

    def __init__(self):
        """Initialize the handler and print CLI instructions."""
        Printer.print_header_app()
        Printer.print_cli_info()

    @staticmethod
    def _check_parentheses_balance(expr: str):
        """Raise `InputError` when parentheses counts do not match."""
        open_count = expr.count("(")
        close_count = expr.count(")")
        if open_count != close_count:
            raise InputError(
                f"Unbalanced parentheses: found {open_count} '(' and {close_count} ')'"
            )

    @staticmethod
    def detect_input_type(text: str) -> str:
        """Detects if an input represents a term or literal using ParserAIMA."""
        kind = ParserAIMA.detect_type(text)
        if kind in {"literal", "literal_negated", "predicate"}:
            return "literal"
        elif kind in {"variable", "constant", "function"}:
            return "term"
        else:
            return "unknown"

    # Read one expression (term or literal)
    def read_expression(self, prompt: str):
        """Reads and parses one user input expression (Term or Literal)."""
        text = input(prompt).strip()
        if text.lower() == "e":
            Printer.print_text_color(
                "\n👋 Thank you for using the Unification CLI!\n",
                color="yellow", bold=True
            )
            exit(0)

        if not text:
            raise InputError(
                "Empty input. Please provide a valid term or literal.")

        # Check parentheses
        self._check_parentheses_balance(text)

        try:
            expr = ParserAIMA.parse_expression(text)
            return expr
        except Exception as e:
            raise InputError(f"Error parsing expression '{text}': {e}")

    # Handle user mode selection
    def interpret_selection(self):
        """
        Prompts user for mode:
          1️⃣ Term unification
          2️⃣ Literal unification
          3️⃣ Auto-detect
          4️⃣ Run all tests
          E️⃣ Exit
        """
        choice = input(
            Printer.get_colored_text("Choose mode (1-Term, 2-Literal, 3-Auto, 4-Tests, E-Exit): ",
                                     color='blue',
                                     bold=True)).strip().lower()

        if choice == "e":
            Printer.continue_or_exit(direct_exit=True)

        if choice == "4":
            Printer.print_grid_run_tests()
            Printer.print_text_color("\n⚙️  Running predefined unification tests ",
                                     color="black", bold=True, end="")
            Printer.print_three_dots()
            run_all_tests()
            Printer.continue_or_exit()

            return self.interpret_selection()  # restart menu

        # Read user expressions
        expr1_raw = input(Printer.get_colored_text(
            "\nWrite the first term/expression: ", color='blue')).strip()
        expr2_raw = input(Printer.get_colored_text(
            "Write the second term/expression: ", color='blue')).strip()

        Printer.print_text_color(
            f"\n⚙️  Running Unification Algorithm for '{expr1_raw}' and '{expr2_raw}' ",
            color="black", bold=True, end=""
        )
        Printer.print_three_dots()

        # Determine mode automatically if needed
        choice = self._auto_set_mode(choice, expr1_raw, expr2_raw)
        return choice, expr1_raw, expr2_raw

    # Decide whether it's literal or term mode automatically
    def _auto_set_mode(self, selection: str, expr1: str, expr2: str) -> str:
        """Resolve ambiguous menu selections by inferring a suitable mode from the inputs."""
        if selection == "3":  # auto-detect
            type1 = self.detect_input_type(expr1)
            type2 = self.detect_input_type(expr2)
            if "literal" in (type1, type2):
                return "2"  # literal unification
            return "1"      # term unification
        return selection

    # Convenience for term-only mode (legacy)
    def read_term(self, prompt: str) -> Term:
        """Legacy mode for backward compatibility (term only)."""
        text = input(prompt).strip()
        if text.lower() == "e":
            Printer.print_goodbye_with_style()
            exit(0)
        self._check_parentheses_balance(text)
        return Term.from_string(text)
