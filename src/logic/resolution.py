from __future__ import annotations

from typing import Optional

from src.logic.substitution import Substitution
from src.logic.unifier import Unifier
from src.models.errors import UnificationError
from src.models.literal import Literal


class Resolution:
    """Minimal resolution helper showcasing how literal unification is orchestrated through the Unifier."""

    def __init__(self):
        """Create a resolution helper with its own `Unifier` instance."""
        self.unifier = Unifier()

    def unify_literals(self, l1: Literal, l2: Literal) -> Optional[Substitution]:
        """Return the substitution that unifies two complementary literals or raise on mismatch."""
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
