from src.io.input_handler import InputHandler
from src.logic.unifier import Unifier
from src.models.errors import UnificationError
from src.models.errors import InputError
from src.utils.printer import Printer
from tests.test_unification import run_all_tests


def main():
    Printer.print_header(header=" " * 20 + "Unification Project - KRPS",
                         domain=" " * 4 + "Knowledge Representation and Problem Solving",
                         extra=" " * 30 + "AIAC1 | Semester 1")
    run_all_tests()

    handler = InputHandler()
    unifier = Unifier()
    delimiter = "-" * 15
    while True:
        try:
            # Read two terms from user input and attempt to unify them.
            t1 = handler.read_term("\n  1️⃣  Write the first term: ")
            t2 = handler.read_term("  2️⃣  Write the second term: ")

            Printer.print_text_color(
                f"\n⚙️  Running Unification Algorithm for \'{t1}\' and \'{t2}\' ",
                color="black",
                bold=True,
                end=""
            )
            Printer.print_three_dots()  # Simulate processing time
            result = unifier.unify(t1, t2)

            if result:
                Printer.print_success(
                    f"Most General Unifier (MGU) = {result}\n")
            else:
                Printer.print_error("\nThe terms cannot be unified.\n")

        except InputError as ie:
            Printer.print_error(f"Error: {ie}")
        except UnificationError as ue:
            Printer.print_error(f"Error: {ue}")
        except Exception as e:  # Catch-all for unexpected errors
            Printer.print_error(f"Error: {e}")


if __name__ == "__main__":
    main()
