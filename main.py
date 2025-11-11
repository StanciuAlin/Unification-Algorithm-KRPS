from src.utils.printer import print_header
from tests.test_unification import run_all_tests


def main():
    print_header(" " * 10 + "Unification Project - KRPS")
    run_all_tests()


if __name__ == "__main__":
    main()
