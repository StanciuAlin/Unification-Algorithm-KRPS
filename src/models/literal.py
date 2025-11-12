from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re
from src.models.term import Term


@dataclass(frozen=True)
class Literal:
    """AIMA-style Literal: a (possibly negated) predicate applied to terms."""

    name: str
    arguments: List[Term]
    negated: bool = False

    # --- Constructors ---
    @staticmethod
    def from_string(text: str) -> Literal:
        """
        Parse a literal from string. Examples:
        - P(x)
        - ¬Loves(John, x)
        - ~SmarterThan(y, z)
        """
        text = text.strip()
        negated = text.startswith("¬") or text.startswith("~")
        if negated:
            text = text[1:].strip()

        match = re.match(r'(\w+)\((.*)\)', text)
        if not match:
            raise ValueError(f"Invalid literal format: {text}")

        name, args_str = match.groups()
        args = Term._split_arguments(args_str)
        parsed_args = [Term.from_string(arg) for arg in args]
        return Literal(name, parsed_args, negated)

    # --- Logic operations ---
    def negate(self) -> Literal:
        """Return the negation of this literal."""
        return Literal(self.name, self.arguments, not self.negated)

    def is_complementary(self, other: Literal) -> bool:
        """Check if this literal and another are complementary (P vs ¬P)."""
        return (
            self.name == other.name
            and len(self.arguments) == len(other.arguments)
            and self.negated != other.negated
        )

    def apply_substitution(self, substitution: 'Substitution') -> Literal:
        """Apply substitution to each argument term."""
        new_args = [arg.apply_substitution(
            substitution) for arg in self.arguments]
        return Literal(self.name, new_args, self.negated)

    def equals(self, other: Literal) -> bool:
        """Check equality of name, negation and arguments."""
        return (
            self.name == other.name
            and self.negated == other.negated
            and all(a1 == a2 for a1, a2 in zip(self.arguments, other.arguments))
        )

    # --- Display ---
    def __str__(self) -> str:
        sign = "¬" if self.negated else ""
        args = ", ".join(str(a) for a in self.arguments)
        return f"{sign}{self.name}({args})"

    def __repr__(self):
        return str(self)
