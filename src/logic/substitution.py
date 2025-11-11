
from __future__ import annotations
from typing import Dict
from dataclasses import dataclass
from src.models.term import Term, Variable


@dataclass
class Substitution:
    """Represents a mapping from variable names to terms."""
    mapping: Dict[str, Term]

    def __init__(self, mapping=None):
        if mapping is None:
            mapping = {}
        self.mapping = dict(mapping)

    def contains(self, var_name: str) -> bool:
        return var_name in self.mapping

    def get(self, var_name: str) -> Term:
        return self.mapping[var_name]

    def extend(self, var_name: str, term: Term) -> 'Substitution':
        new_map = dict(self.mapping)
        new_map[var_name] = term
        return Substitution(new_map)

    def apply(self, term: Term) -> Term:
        return term.apply_substitution(self)

    def compose(self, other: 'Substitution') -> 'Substitution':
        """Compose two substitutions: apply other, then self."""
        new_map = {v: self.apply(t) for v, t in other.mapping.items()}
        for v, t in self.mapping.items():
            new_map[v] = t
        return Substitution(new_map)

    def is_empty(self) -> bool:
        return len(self.mapping) == 0

    def __str__(self):
        if not self.mapping:
            return "{}"
        # pairs = [f"{v} -> {t}" for v, t in self.mapping.items()]
        pairs = [f"{t} / {v}" for v, t in self.mapping.items()]
        return "{ " + ", ".join(pairs) + " }"
