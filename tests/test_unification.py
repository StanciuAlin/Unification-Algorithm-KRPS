from src.models.term import Variable, Constant, Function
from src.logic.unifier import Unifier
from src.logic.resolution import Literal, ResolutionHelper
from src.models.errors import UnificationError


def run_all_tests():
    u = Unifier()
    print("Running Unification Tests...")

    # 1. X = a
    try:
        print("\n\nTest 1: Unifying X and a")
        s1 = u.unify(Variable("X"), Constant("a"))
        print("    Unifier =", s1)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 2. X = Y
    try:
        print("\nTest 2: Unifying X and Y")
        s2 = u.unify(Variable("X"), Variable("Y"))
        print("    Unifier =", s2)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 3. a = a
    try:
        print("\nTest 3: Unifying a and a")
        s3 = u.unify(Constant("a"), Constant("a"))
        print("    Unifier =", s3)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 4. a = b (fail)
    try:
        print("\nTest 4: Unifying a and b")
        s4 = u.unify(Constant("a"), Constant("b"))
        print("    Unifier =", s4)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 5. f(X) = f(a) -> X = a
    try:
        print("\nTest 5: Unifying f(X) and f(a)")
        s5 = u.unify(Function("f", [Variable("X")]),
                     Function("f", [Constant("a")]))
        print("    Unifier =", s5)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 6. g(X, b) = g(a, b) -> X = a
    try:
        print("\nTest 6: Unifying g(X, b) and g(a, b)")
        s6 = u.unify(Function("g", [Variable("X"), Constant("b")]),
                     Function("g", [Constant("a"), Constant("b")]))
        print("    Unifier =", s6)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 7. h(f(X), b) = h(f(a), b) -> X = a
    try:
        print("\nTest 7: Unifying h(f(X), b) and h(f(a), b)")
        s7 = u.unify(Function("h", [Function("f", [Variable("X")]), Constant("b")]),
                     Function("h", [Function("f", [Constant("a")]), Constant("b")]))
        print("    Unifier =", s7)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 8. occurs check: X = f(X) -> fail
    try:
        print("\nTest 8: Unifying X and f(X)")
        s8 = u.unify(Variable("X"), Function("f", [Variable("X")]))
        print("    Unifier =", s8)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 9. parent(john, X) = parent(john, mary) -> X = mary
    try:
        print("\nTest 9: Unifying parent(john, X) and parent(john, mary)")
        s9 = u.unify(Function("parent", [Constant("john"), Variable("X")]),
                     Function("parent", [Constant("john"), Constant("mary")]))
        print("    Unifier =", s9)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 10. resolution-style: P(X,a) and ¬P(b,a) -> X = b
    try:
        print("\nTest 10: Unifying literals P(X,a) and ¬P(b,a)")
        rh = ResolutionHelper()
        lit1 = Literal("P", [Variable("X"), Constant("a")], negated=False)
        lit2 = Literal("P", [Constant("b"), Constant("a")], negated=True)
        s10 = rh.unify_literals(lit1, lit2)
        print("    Unifier =", s10)
    except UnificationError as e:
        print("\tUnificationError:", e)


if __name__ == "__main__":
    run_all_tests()
