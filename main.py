from src.io.input_handler import InputHandler
from src.logic.unifier import Unifier
from src.models.errors import UnificationError
from src.models.errors import InputError
from src.utils.printer import print_header
from tests.test_unification import run_all_tests


def main():
    print_header(header=" " * 20 + "Unification Project - KRPS",
                 domain="📚 Knowledge Representation and Problem Solving",
                 extra=" " * 26 + "🎓 AIAC1 | Semester 1")
    run_all_tests()

    handler = InputHandler()
    unifier = Unifier()
    delimiter = "-" * 15
    while True:
        try:
            # Read two terms from user input and attempt to unify them.
            t1 = handler.read_term("1️⃣ Write the first term: ")
            t2 = handler.read_term("2️⃣ Write the second term: ")

            print(
                f"\n🔍 Running Unification Algorithm for \'{t1}\' and \'{t2}\'")
            result = unifier.unify(t1, t2)

            if result:
                print(
                    f"\n✅ Most General Unifier (MGU) = {result}\n{delimiter}\n")
            else:
                print("\n❌ The terms cannot be unified.\n")

        except InputError as ie:
            print(f"⚠️  Input error: {ie}\n")
        except UnificationError as ue:
            print(f"⚠️  Unification failed: {ue}\n")
        except Exception as e:  # Catch-all for unexpected errors
            print(f"⚠️  Error: {e}\n")


if __name__ == "__main__":
    main()
