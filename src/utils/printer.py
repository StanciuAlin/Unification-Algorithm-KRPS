from colorama import Fore, Style, init
import time

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
    """Utility printer for styling CLI messaging throughout the project."""

    SEPARATOR_LENGTH = 75

    @staticmethod
    def print_header(header: str, domain: str = "KRPS", extra: str = ""):
        """Prints a large header block for CLI sections."""
        separator = "=" * Printer.SEPARATOR_LENGTH
        Printer.print_text_color("\n\n" + separator, color="green", bold=True)
        Printer.print_text_color(header, color="green", bold=True)
        Printer.print_text_color(f"\n\t\t{domain}", color="yellow", bold=True)
        if extra:
            Printer.print_text_color(f"\t\t{extra}", color="yellow", bold=True)
        Printer.print_text_color(separator + "\n\n", color="green", bold=True)

    @staticmethod
    def print_title(title: str):
        """Prints a section title surrounded by separators."""
        separator = "=" * Printer.SEPARATOR_LENGTH + '\n'
        Printer.print_text_color(
            "\n\n" + separator, color="green", bold=True, end="")
        Printer.print_text_color(title, color="green", bold=True)
        Printer.print_text_color(
            separator, color="green", bold=True, end="\n\n")

    @staticmethod
    def print_cli_info():
        """Prints the AIMA convention info for variable, constant, and predicate notation."""

        Printer.print_text_color(
            "Write two logical propositions to unify them.", color="blue", bold=True)
        Printer.print_text_color(
            "\tExample: king(X), king(john)", color="black")
        Printer.print_text_color(
            "\tExample: loves(john, X), loves(Y, mary)", color="black")

        Printer.print_text_color(
            "Convention (Russell & Norvig - AIMA, 4th Ed.):", color="blue", bold=True)
        Printer.print_text_color(
            "\tConstants → lowercase  (john, mary, a, b)", color="black")
        Printer.print_text_color(
            "\tVariables → uppercase  (X, Y, Z)", color="black")
        Printer.print_text_color(
            "\tFunctions/Predicates → lowercase  (king(X), loves(john, X))", color="black")

        Printer.print_text_color(
            "Type 'e' or 'E' to exit.", color="blue", bold=True)

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
        """Prints an informational message in cyan."""
        Printer.print_text_color(
            f"   {message}", color="cyan", bold=False, end="")

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
