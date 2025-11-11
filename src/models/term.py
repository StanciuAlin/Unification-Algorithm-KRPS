from __future__ import annotations
from dataclasses import dataclass
from typing import List, Any
import re


class Term:
    """Base class for all terms in FOL."""

    def occurs(self, var_name: str) -> bool:
        raise NotImplementedError

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        raise NotImplementedError

    @staticmethod
    def from_string(text: str) -> 'Term':
        """
        Creates a Term object from its string representation. Examples:
        - King(x)
        - Loves(John, y)
        - John
        - x
        """
        text = text.strip()

        # Case 1: Constant or simple variable
        if "(" not in text:
            if text and text[0].isupper():
                return Constant(text)
            else:
                return Variable(text)

        # Case 2: Function or predicate with arguments
        match = re.match(r'(\w+)\((.*)\)', text)
        if not match:
            raise ValueError(f"Invalid format for term: {text}")

        name, args_str = match.groups()
        args = []

        # Split arguments by commas, handling nested functions (without unuseful spaces)
        for arg in args_str.split(","):
            arg = arg.strip()
            if arg:
                args.append(Term.from_string(arg))

        return Function(name, args)

    def __repr__(self):
        return str(self)


@dataclass(frozen=True)
class Variable(Term):
    name: str

    def occurs(self, var_name: str) -> bool:
        return self.name == var_name

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        if substitution.contains(self.name):
            return substitution.get(self.name).apply_substitution(substitution)
        return self

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Constant(Term):
    value: Any

    def occurs(self, var_name: str) -> bool:
        return False

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        return self

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Function(Term):
    name: str
    arguments: List[Term]

    def occurs(self, var_name: str) -> bool:
        return any(arg.occurs(var_name) for arg in self.arguments)

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        new_args = [arg.apply_substitution(
            substitution) for arg in self.arguments]
        return Function(self.name, new_args)

    def __str__(self) -> str:
        if not self.arguments:
            return self.name
        return f"{self.name}(" + ", ".join(str(a) for a in self.arguments) + ")"
