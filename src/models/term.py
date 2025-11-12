from __future__ import annotations
from dataclasses import dataclass
from typing import List, Any
import re


class Term:
    """Base class for all terms in First-Order Logic (AIMA convention)."""

    def occurs(self, var_name: str) -> bool:
        """Check if a variable occurs inside the term."""
        raise NotImplementedError

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        """Apply a substitution mapping to this term."""
        raise NotImplementedError

    @staticmethod
    def from_string(text: str) -> 'Term':
        """
        Parse a term from string using AIMA-style syntax.
        Examples:
        - Father(John, x)
        - Loves(Mary, y)
        - John
        - x
        """
        text = text.strip()

        # Case 1: atomic symbol (no parentheses)
        if "(" not in text:
            if text[0].islower():
                return Variable(text)
            else:
                return Constant(text)

        # Case 2: function term
        match = re.match(r'(\w+)\((.*)\)', text)
        if not match:
            raise ValueError(f"Invalid term format: {text}")

        name, args_str = match.groups()
        args = Term._split_arguments(args_str)
        parsed_args = [Term.from_string(arg) for arg in args]
        return Function(name, parsed_args)

    @staticmethod
    def _split_arguments(args_str: str) -> List[str]:
        """Split arguments while respecting nested parentheses."""
        args, current, depth = [], "", 0
        for char in args_str:
            if char == ',' and depth == 0:
                args.append(current.strip())
                current = ""
            else:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                current += char
        if current.strip():
            args.append(current.strip())
        return args

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
    symbol: Any

    def occurs(self, var_name: str) -> bool:
        return False

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        return self

    def __str__(self) -> str:
        return str(self.symbol)


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
