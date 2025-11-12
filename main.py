import time
from src.io.input_handler import InputHandler
from src.logic.parser import ParserAIMA
from src.logic.unifier import Unifier
from src.models.errors import UnificationError, InputError
from src.utils.printer import Printer


def main():

    handler = InputHandler()
    unifier = Unifier(verbose=False)

    Printer.print_header_app()

    while True:
        Printer.print_menu()
        choice, expr1, expr2 = handler.interpret_selection()

        try:
            # TERM UNIFICATION
            if choice == "1":
                Printer.print_info("Mode: Term Unification\n")
                t1 = ParserAIMA.parse_term(expr1)
                t2 = ParserAIMA.parse_term(expr2)

                result = unifier.unify(t1, t2)
                if result and not result.is_empty():
                    Printer.print_success(
                        f"✅ Most General Unifier (MGU): {result}\n")
                else:
                    Printer.print_error("❌ The terms cannot be unified.\n")

            # LITERAL UNIFICATION
            elif choice == "2":
                Printer.print_info("Mode: Literal Unification\n")
                l1 = ParserAIMA.parse_literal(expr1)
                l2 = ParserAIMA.parse_literal(expr2)

                result = unifier.unify_literals(l1, l2)
                if result:
                    Printer.print_success(
                        f"✅ Literals unified successfully: {result}\n")
                else:
                    Printer.print_error("❌ Literals cannot be unified.\n")

            # INVALID / UNEXPECTED CHOICE
            else:
                Printer.print_text_color(
                    "  Invalid choice. Please select 1, 2, 3, 4 or E.", "yellow"
                )

        except InputError as ie:
            Printer.print_error(f"  Input Error: {ie}")
        except UnificationError as ue:
            Printer.print_error(f"❌ Unification Error: {ue}")
        except Exception as e:
            Printer.print_error(f"  Unexpected Error: {e}")

        Printer.continue_or_exit()


if __name__ == "__main__":
    main()
