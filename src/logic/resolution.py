from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Union
from src.models.term import Term, Function
from src.logic.unifier import Unifier
from src.logic.substitution import Substitution
from src.models.errors import UnificationError


@dataclass(frozen=True)
class Literal:
    name: str
    arguments: List[Term]
    negated: bool = False

    def negate(self) -> 'Literal':
        return Literal(self.name, self.arguments, not self.negated)

    def __str__(self):
        sign = "¬" if self.negated else ""
        args = ", ".join(str(a) for a in self.arguments)
        return f"{sign}{self.name}({args})"


class ResolutionHelper:
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
