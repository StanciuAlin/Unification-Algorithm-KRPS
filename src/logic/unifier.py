from __future__ import annotations

from typing import Optional

from src.logic.substitution import Substitution
from src.models.errors import UnificationError
from src.models.literal import Literal
from src.models.term import Function, Term, Variable
from src.utils.printer import Printer


class Unifier:
    """Deterministic implementation of the AIMA unification procedure for both terms and literals."""

    def __init__(self, verbose: bool = False):
        """Initialize the unifier; enable verbose printing when `verbose` is True."""
        self.verbose = verbose

    # UNIFY for Terms
    def unify(self, t1: Term, t2: Term, subst: Optional[Substitution] = None) -> Substitution:
        """Main unification entry point for terms."""
        if subst is None:
            subst = Substitution()

        # Always apply current substitution to both sides
        t1 = subst.apply(t1)
        t2 = subst.apply(t2)

        # Equal terms => done
        if t1 == t2:
            return subst

        # Case: Variable
        if isinstance(t1, Variable):
            return self._unify_var(t1, t2, subst)
        if isinstance(t2, Variable):
            return self._unify_var(t2, t1, subst)

        # Case: Function or compound term
        if isinstance(t1, Function) and isinstance(t2, Function):
            if t1.name != t2.name or len(t1.arguments) != len(t2.arguments):
                raise UnificationError(
                    f"Cannot unify {t1} and {t2}: different function symbols or arity"
                )

            for a1, a2 in zip(t1.arguments, t2.arguments):
                # 🔹 Propagate substitutions at each step
                a1 = subst.apply(a1)
                a2 = subst.apply(a2)
                subst = self.unify(a1, a2, subst)
            return subst

        # Otherwise → failure
        raise UnificationError(f"Cannot unify {t1} with {t2}")

    # UNIFY for Literals (with negation)
    def unify_literals(self, l1: Literal, l2: Literal, subst: Optional[Substitution] = None) -> Optional[Substitution]:
        """Unify two complementary literals."""
        if subst is None:
            subst = Substitution()

        # Must be complementary
        if l1.name != l2.name or len(l1.arguments) != len(l2.arguments):
            return None
        if l1.negated == l2.negated:
            return None

        # Unify all arguments
        for a1, a2 in zip(l1.arguments, l2.arguments):
            a1 = subst.apply(a1)
            a2 = subst.apply(a2)
            subst = self.unify(a1, a2, subst)
        return subst

    # Variable handling and occurs check
    def _unify_var(self, var: Variable, term: Term, subst: Substitution) -> Substitution:
        """Handle variable unification cases."""
        if subst.contains(var.name):
            return self.unify(subst.get(var.name), term, subst)
        if isinstance(term, Variable) and subst.contains(term.name):
            return self.unify(var, subst.get(term.name), subst)

        # Occurs check (prevent infinite recursion)
        if self._occurs_check(var, term):
            raise UnificationError(
                f"Occurs check failed: variable '{var}' occurs in term '{term}'"
            )

        # Important: apply substitution to term before extending
        term = subst.apply(term)
        return subst.extend(var.name, term)

    def _occurs_check(self, var: Variable, term: Term) -> bool:
        """Check if variable occurs in term (prevents self-reference)."""
        return term.occurs(var.name)

    # Utility and debugging
    def debug(self, msg: str):
        """Print a debug message when verbose mode is enabled."""
        if self.verbose:
            Printer.print_text_color("cyan", msg)
