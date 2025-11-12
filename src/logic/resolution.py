from __future__ import annotations
from typing import Optional, Union
from src.models.literal import Literal
from src.models.term import Function
from src.logic.unifier import Unifier
from src.logic.substitution import Substitution
from src.models.errors import UnificationError


class Resolution:
    """Very small example to show how unification is used in resolution."""

    def __init__(self):
        self.unifier = Unifier()

    def unify_literals(self, l1: Literal, l2: Literal) -> Optional[Substitution]:
        # must be complementary
        if l1.name != l2.name or len(l1.arguments) != len(l2.arguments):
            raise UnificationError(f"Cannot unify literals {l1} and {l2}")
        if l1.negated == l2.negated:
            raise UnificationError(
                f"Literals {l1} and {l2} are not complementary")

        subst = Substitution()
        for a1, a2 in zip(l1.arguments, l2.arguments):
            subst = self.unifier.unify(a1, a2, subst)
        return subst
