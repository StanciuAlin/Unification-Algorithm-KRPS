from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from src.models.term import Term, Variable


@dataclass(frozen=True)
class Substitution:
    """Immutable mapping from variable names to replacement terms used to build most-general unifiers."""

    mapping: Dict[str, Term]

    def __init__(self, mapping: Dict[str, Term] | None = None):
        """Create a substitution; copies `mapping` to keep instances immutable."""
        object.__setattr__(self, "mapping", dict(mapping or {}))

    # Basic accessors
    def contains(self, var_name: str) -> bool:
        """Return True if the variable name exists in the substitution."""
        return var_name in self.mapping

    def get(self, var_name: str) -> Term:
        """Return the term currently mapped to `var_name`."""
        return self.mapping[var_name]

    def is_empty(self) -> bool:
        """Return True if the substitution contains no mappings."""
        return len(self.mapping) == 0

    # Core operations
    def extend(self, var_name: str, term: Term) -> Substitution:
        """
        Return a new substitution extended with {var_name / term}.
        Avoid self-mapping (x/x) to prevent infinite recursion.
        """
        if isinstance(term, Variable) and term.name == var_name:
            return self  # no change
        new_map = dict(self.mapping)
        new_map[var_name] = term
        return Substitution(new_map)

    def apply(self, term: Term) -> Term:
        """Apply this substitution to a term."""
        return term.apply_substitution(self)

    def apply_to_literal(self, literal: 'Literal') -> 'Literal':
        """Apply substitution to a literal."""
        return literal.apply_substitution(self)

    def compose(self, other: Substitution) -> Substitution:
        """
        Compose two substitutions: self ∘ other means
        apply self, then apply other to the result.
        """
        # Apply self to all terms in other
        composed = {v: self.apply(t) for v, t in other.mapping.items()}
        # Add mappings from self
        for v, t in self.mapping.items():
            composed[v] = t
        return Substitution(composed)

    # String representation
    def __str__(self) -> str:
        """Return the substitution in `{ var / term }` notation."""
        if not self.mapping:
            return "{}"
        # Here can be {t} / {v} depending on preference
        # But, usually written as {v / t} according to AIMA style
        # Is read as "variable v is substituted/replaced by term t"
        pairs = [f"{var} / {term}" for var, term in self.mapping.items()]
        return "{ " + ", ".join(pairs) + " }"

    def __repr__(self):
        """Return the developer representation mirroring `__str__`."""
        return str(self)
