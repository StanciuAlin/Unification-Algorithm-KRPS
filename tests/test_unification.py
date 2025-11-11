from src.models.term import Variable, Constant, Function
from src.logic.unifier import Unifier
from src.logic.resolution import Literal, ResolutionHelper
from src.models.errors import UnificationError


def run_all_tests():
    u = Unifier()
    print("Running Unification tests...")

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

    # 11. King(x), King(John) -> x = John
    try:
        print("\nTest 11: Unifying King(x) and King(John)")
        s11 = u.unify(Function("King", [Variable("x")]),
                      Function("King", [Constant("John")]))
        print("    Unifier =", s11)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 12. even(4), even(X) -> X = 4
    try:
        print("\nTest 12: Unifying even(4) and even(X)")
        s12 = u.unify(Function("even", [Variable("4")]),
                      Function("even", [Constant("X")]))
        print("    Unifier =", s12)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 13. MGU of q(a, Y, h(k(W))) and q(W, h(Z), h(Z)) -> W = a, Y = h(a), Z = k(a)
    try:
        print("\nTest 13: Unifying q(a, Y, h(k(W))) and q(W, h(Z), h(Z))")
        s13 = u.unify(
            Function("q", [Constant("a"), Variable("Y"), Function(
                "h", [Function("k", [Variable("W")])])]),
            Function("q", [Variable("W"), Function(
                "h", [Variable("Z")]), Function("h", [Variable("Z")])])
        )
        print("    Unifier =", s13)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 14. likes(Sarah, Y) and likes(Sarah, chocolate) -> Y = chocolate
    try:
        print("\nTest 14: Unifying likes(Sarah, Y) and likes(Sarah, chocolate)")
        s14 = u.unify(
            Function("likes", [Constant("Sarah"), Variable("Y")]),
            Function("likes", [Constant("Sarah"), Constant("chocolate")])
        )
        print("    Unifier =", s14)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 15. {p(b, X, f(g(Z))) and p(Z, f(Y), f(Y))} -> {X=f(Y), Z=b}
    try:
        print("\nTest 15: Unifying p(b, X, f(g(Z))) and p(Z, f(Y), f(Y))")
        s15 = u.unify(
            Function("p", [Constant("b"), Variable("X"), Function(
                "f", [Function("g", [Variable("Z")])])]),
            Function("p", [Variable("Z"), Function(
                "f", [Variable("Y")]), Function("f", [Variable("Y")])])
        )
        print("\nTest 15:", s15)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 16. {p(f(a), g(Y)) and p(X, X)} -> fail
    try:
        s16 = u.unify(
            Function("p", [Function("f", [Constant("a")]),
                           Function("g", [Variable("Y")])]),
            Function("p", [Variable("X"), Variable("X")])
        )
        print("\nTest 16:", s16)
    except UnificationError as e:
        print("\tUnificationError:", e)

    # 17. Q(a, g(x, a), f(y)), Q(a, g(f(b), a), x)} -> {x=f(b), y=f(f(b))}
    try:
        print("\nTest 17: Unifying Q(a, g(x, a), f(y)) and Q(a, g(f(b), a), x)")
        s17 = u.unify(
            Function("Q", [Constant("a"), Function(
                "g", [Variable("x"), Constant("a")]), Function("f", [Variable("y")])]),
            Function("Q", [Constant("a"), Function(
                "g", [Function("f", [Constant("b")]), Constant("a")]), Variable("x")])
        )
        print("    Unifier =", s17)
    except UnificationError as e:
        print("\tUnificationError:", e)


if __name__ == "__main__":
    run_all_tests()
