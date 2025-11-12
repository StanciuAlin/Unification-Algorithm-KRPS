from src.logic.parser import ParserAIMA
from src.logic.unifier import Unifier
from src.models.errors import UnificationError
from src.models.literal import Literal
from src.models.term import Constant, Function, Variable
from src.utils.printer import Printer


def run_all_tests():
    """Execute the curated suite of term and literal unification demonstrations."""
    u = Unifier()
    p = ParserAIMA()

    # TERM tests

    Printer.print_title("Term Unification Tests")
    term_tests = [
        # Correct unifications
        ("X", "a", "{ X / a }"),
        ("x", "y", "{ x / y }"),
        ("a", "a", "{}"),
        ("f(X)", "f(a)", "{ X / a }"),
        ("g(X, b)", "g(a, b)", "{ X / a }"),
        ("h(f(X), b)", "h(f(a), b)", "{ X / a }"),
        ("parent(john, X)", "parent(john, mary)", "{ X / mary }"),
        ("king(X)", "king(john)", "{ X / john }"),
        ("even(x)", "even(4)", "{ X / 4 }"),
        ("p(X, X)", "p(a, a)", "{ X / a }"),

        # Expected failures
        ("A", "B", "Cannot unify A with B"),
        ("X", "f(X)", "Cannot unify X with f(X)"),
        ("p(f(a), g(Y))", "p(X, X)", "Cannot unify f(a) with X"),
    ]

    term_success = 0
    for idx, (t1, t2, expected) in enumerate(term_tests, start=1):
        Printer.print_text_color(f"[{idx:02}] {t1}  |  {t2}", color="gray")
        try:
            s = u.unify(p.parse_term(t1), p.parse_term(t2))
            Printer.print_text_color(f"    Result: {s}", color="green")
            term_success += 1
        except UnificationError as e:
            Printer.print_text_color(f"    Error: {str(e)}", color="red")
        Printer.print_text_color(
            f"    Expected: {expected}", color="blue",  end="\n\n")

    # LITERAL tests

    Printer.print_title("Literal Unification Tests")

    literal_tests = [
        # Correct literal unifications
        ("P(X, a)", "~P(b, a)", "{ X / b }"),
        ("Knows(richard, X)", "~Knows(richard, john)", "{ X / john }"),
        ("Loves(sarah, Y)", "~Loves(sarah, chocolate)", "{ Y / chocolate }"),
        ("Ancestor(X, Y)", "~Ancestor(bob, Y)", "{ X / bob }"),
        ("R(f(X), g(Y))", "~R(f(a), g(b))", "{ X / a, Y / b }"),
        ("Hates(X, Y)", "~Hates(john, mary)", "{ X / john, Y / mary }"),
        ("S(X, Y, Z)", "~S(a, Y, Z)", "{ X / a }"),
        ("Q(X, X)", "~Q(a, a)", "{ X / a }"),

        # Expected failures
        ("P(f(X), Y)", "~P(Z, f(a))", "Cannot unify f(X) with Z"),
        ("Q(a, g(X, a), f(Y))", "~Q(a, g(f(b), a), X)", "Cannot unify X with f(b)"),
        ("P(X, a)", "P(b, a)", "Cannot be unified"),
        ("Knows(richard, X)", "~Loves(richard, john)", "Cannot be unified"),
        ("R(X)", "~R(f(X))", "Cannot unify X with f(X)"),
    ]

    literal_success = 0
    for idx, (l1, l2, expected) in enumerate(literal_tests, start=len(term_tests) + 1):
        Printer.print_text_color(f"[{idx:02}] {l1}  |  {l2}", color="gray")
        try:
            lit1 = p.parse_literal(l1)
            lit2 = p.parse_literal(l2)
            s = u.unify_literals(lit1, lit2)
            if s is None:
                Printer.print_text_color(
                    "    Result: Cannot be unified", color="red")
            else:
                Printer.print_text_color(f"    Result: {s}", color="green")
                literal_success += 1
        except UnificationError as e:
            Printer.print_text_color(f"    Error: {str(e)}", color="red")
        Printer.print_text_color(
            f"    Expected: {expected}", color="blue", end="\n\n")

    # Summary

    Printer.print_title("Test Summary")
    term_total = len(term_tests)
    literal_total = len(literal_tests)
    total_success = term_success + literal_success
    total_tests = term_total + literal_total
    percent = (total_success / total_tests) * 100

    Printer.print_text_color(
        f"Term tests passed: {term_success}/{term_total}", color="cyan")
    Printer.print_text_color(
        f"Literal tests passed: {literal_success}/{literal_total}", color="cyan")
    Printer.print_text_color(
        f"Total passed: {total_success}/{total_tests}  ({percent:.0f}%)", color="green", bold=True, end="\n\n")


if __name__ == "__main__":
    run_all_tests()
