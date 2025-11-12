import time

from colorama import Fore, Style, init

# Initialize colorama (so colors reset automatically after each print)
init(autoreset=True)

COLORS = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "white": Fore.WHITE,
    "black": Fore.BLACK,
    "gray": Fore.LIGHTBLACK_EX,
    "reset": Style.RESET_ALL,
}


class Printer:
    """Centralized helper that prints colored, styled CLI messages and shared UI widgets for the app."""

    SEPARATOR_LENGTH = 75

    @staticmethod
    def print_header_app():
        """Prints a large header block for CLI sections."""
        separator = "=" * Printer.SEPARATOR_LENGTH
        Printer.print_text_color("\n\n" + separator, color="green", bold=True)
        Printer.print_text_color(
            " " * 18 + "Unification Algorithm - KRPS Project", color="green", bold=True)
        Printer.print_text_color(
            "\n\t" + " " * 23 + "Knowledge Representation and Problem Solving", color="yellow", bold=True)
        Printer.print_text_color(
            "\t\t" + " " * 12 + "AIAC1 | Semester 1 | ACE, University of Craiova", color="yellow", bold=True)
        Printer.print_text_color(separator + "\n\n", color="green", bold=True)

    @staticmethod
    def print_title(title: str):
        """Prints a section title surrounded by separators."""
        title = Printer.get_text_centered_between_n_chars(
            title, Printer.SEPARATOR_LENGTH, " ")
        separator = "-" * Printer.SEPARATOR_LENGTH
        Printer.print_text_color(
            "\n" + separator, color="blue", bold=True)
        Printer.print_text_color(title, color="blue", bold=True)
        Printer.print_text_color(
            separator, color="blue", bold=True, end="\n\n")

    @staticmethod
    def print_cli_info():
        """Prints the AIMA convention info for variable, constant, and predicate notation."""

        Printer.print_text_color(
            "Write two logical propositions or literals to unify them.", color="blue", bold=True)
        Printer.print_text_color(
            "\tExample 1: king(X), king(john)", color="black")
        Printer.print_text_color(
            "\tExample 2: loves(john, X), loves(Y, mary)", color="black")
        Printer.print_text_color(
            "\tExemple 3: ¬Loves(John, x) sau ~Animal(y)", color="black")

        Printer.print_text_color(
            "Convention (Russell & Norvig - AIMA, 4th Ed.):", color="blue", bold=True)
        Printer.print_text_color(
            "\tVariable: lowercase, without paranthesis (john, mary, a, b)", color="black")
        Printer.print_text_color(
            "\tConstants: uppercase, without paranthesis  (X, Y, Z)", color="black")
        Printer.print_text_color(
            "\tFunction: lowercase, with paranthesis  (king(X), loves(john, X))", color="black")
        Printer.print_text_color(
            "\tPredicate: uppercase, with paranthesis  (Loves(John, x), Animal(Tom))", color="black")
        Printer.print_text_color(
            "\tNegation: prefix symbols ¬ or ~  (¬Loves(John, x), ~Animal(y))", color="black")

    @staticmethod
    def print_menu():
        """Prints the main menu options."""
        menu_title = Printer.get_text_centered_between_n_chars(
            " MAIN MENU ", Printer.SEPARATOR_LENGTH, "-")
        Printer.print_text_color(
            "\n" + menu_title, color="blue", bold=True, end="\n")
        print("\t1️⃣  Unify simple terms")
        print("\t2️⃣  Unify literals (predicates, possibly negated)")
        print("\t3️⃣  Auto-detect based on input format")
        print("\t4️⃣  Run predefined tests")
        print("\t👋 Exit")
        Printer.print_dash_line()

    @staticmethod
    def print_grid_run_tests():
        """Prints the main menu options."""
        grid_title = Printer.get_text_centered_between_n_chars(
            " RUN TESTS ", Printer.SEPARATOR_LENGTH, "-")
        Printer.print_text_color(
            "\n" + grid_title, color="blue", bold=True, end="\n")

    @staticmethod
    def get_text_centered_between_n_chars(message: str, n: int = SEPARATOR_LENGTH, ch_sep: str = " ") -> str:
        """Returns a string centered between n characters."""
        left = (int((n - len(message)) / 2))
        right = n - left - len(message)
        return ch_sep * left + message + ch_sep * right

    @staticmethod
    def print_text_color(message: str, color: str = "reset", bold: bool = False, end: str = "\n"):
        """
        Prints a message in a given color using colorama.

        Args:
            message (str): The text to print.
            color (str): Color name (red, green, yellow, blue, cyan, magenta, white, gray).
            bold (bool): If True, text is printed in bold.
            end (str): End character (default newline).
        """
        color_code = COLORS.get(color.lower(), Style.RESET_ALL)
        style = Style.BRIGHT if bold else ""
        print(f"{style}{color_code}{message}{Style.RESET_ALL}", end=end)

    @staticmethod
    def get_colored_text(message: str, color: str = "reset", bold: bool = False) -> str:
        """
        Returns a string with ANSI color codes for the given message.

        Args:
            message (str): The text to color.
            color (str): Color name (red, green, yellow, blue, cyan, magenta, white, gray).
            bold (bool): If True, text is bold.

        Returns:
            str: The colored text with ANSI codes.
        """
        color_code = COLORS.get(color.lower(), Style.RESET_ALL)
        style = Style.BRIGHT if bold else ""
        return f"{style}{color_code}{message}{Style.RESET_ALL}"

    @staticmethod
    def print_error(message: str):
        """Prints an error message in red with line spacing."""
        Printer.print_text_color(
            f"   {message}\n", color="red", bold=True, end="")

    @staticmethod
    def print_success(message: str):
        """Prints a success message in green."""
        Printer.print_text_color(
            f"   {message}", color="green", bold=True, end="")

    @staticmethod
    def print_warning(message: str):
        """Prints a warning message in yellow."""
        Printer.print_text_color(
            f"   {message}", color="yellow", bold=True, end="")

    @staticmethod
    def print_info(message: str):
        """Prints an informational message in blue."""
        Printer.print_text_color(
            f"   {message}", color="blue", bold=False, end="")

    @staticmethod
    def print_three_dots(lapse: float = 1.2):
        """Prints three dots with a slight delay to simulate processing."""
        if lapse <= 0:
            lapse = 1.2  # Default lapse time
        wait_time = lapse / 3
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(wait_time)
        print('\n')  # New line after dots

    @staticmethod
    def print_dash_line():
        """Prints a dashed line separator."""
        Printer.print_text_color(
            "-" * Printer.SEPARATOR_LENGTH,
            color="blue",
            bold=True,
            end="\n\n")

    @staticmethod
    def continue_or_exit(direct_exit: bool = False):
        """Prompts the user to continue or exit the application."""
        Printer.print_dash_line()
        if direct_exit:
            Printer.print_goodbye_with_style()
            exit(0)
        Printer.print_info("Press Enter to continue or 'E' to exit.")
        cont = input().strip().lower()
        if cont == "e":
            time.sleep(0.5)
            Printer.print_dash_line()
            Printer.print_goodbye_with_style()
            exit(0)

    @staticmethod
    def print_goodbye():
        """Prints a goodbye message."""
        Printer.print_text_color(
            "\n👋 Thank you for using the Unification CLI! Exiting Unification CLI.",
            color="yellow", bold=True
        )

    @staticmethod
    def print_goodbye_with_style():
        """Prints a styled goodbye message."""
        Printer.print_title(
            "👋 Thank you for using the Unification CLI! Exiting Unification CLI.")
