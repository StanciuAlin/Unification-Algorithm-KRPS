from __future__ import annotations
from typing import Optional
from src.models.term import Term, Variable, Function
from src.logic.substitution import Substitution
from src.models.errors import UnificationError


class Unifier:
    """Implements the unification algorithm for FOL terms."""

    # -> Optional[Substitution]:
    def unify(self, t1: Term, t2: Term, subst: Optional[Substitution] = None):
        if subst is None:
            subst = Substitution()

        # Apply current substitution
        t1 = subst.apply(t1)
        t2 = subst.apply(t2)

        # If equal -> done
        if str(t1) == str(t2):
            return subst

        # Variable cases
        if isinstance(t1, Variable):
            return self._unify_var(t1, t2, subst)
        if isinstance(t2, Variable):
            return self._unify_var(t2, t1, subst)

        # Function / compound case
        if isinstance(t1, Function) and isinstance(t2, Function):
            if t1.name != t2.name or len(t1.arguments) != len(t2.arguments):
                raise UnificationError(
                    "Unification failed (different function symbols)", t1, t2)
            for arg1, arg2 in zip(t1.arguments, t2.arguments):
                subst = self.unify(arg1, arg2, subst)
                if subst is None:
                    raise UnificationError(
                        f"Unification failed between {t1} and {t2}")
            return subst

        # Constants or incompatible terms
        raise UnificationError(
            "Unification failed (Constants or incompatible terms)", t1, t2)

    def _unify_var(self, var: Variable, term: Term, subst: Substitution) -> Optional[Substitution]:
        # if variable already substituted
        if subst.contains(var.name):
            return self.unify(subst.get(var.name), term, subst)

        # occurs check
        if term.occurs(var.name):
            raise UnificationError(
                f"Occurs check failed: {var} occurs in {term}")

        # extend substitution
        return subst.extend(var.name, term)
