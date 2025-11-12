from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, List


class Term:
    """Abstract base for every syntactic term (variable, constant, or function) handled by the unifier."""

    def occurs(self, var_name: str) -> bool:
        """Return True if the variable `var_name` occurs anywhere inside the term."""
        raise NotImplementedError

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        """Return a copy of the term with `substitution` applied recursively."""
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
        """Return formal representation that mirrors `__str__` for debugging."""
        return str(self)


@dataclass(frozen=True)
class Variable(Term):
    """First-order logic variable identified by a lowercase symbol and acting as a unification placeholder."""

    name: str

    def occurs(self, var_name: str) -> bool:
        """Return True when `var_name` matches this variable's name."""
        return self.name == var_name

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        """Return the substituted term if present; otherwise return the variable."""
        if substitution.contains(self.name):
            return substitution.get(self.name).apply_substitution(substitution)
        return self

    def __str__(self) -> str:
        """Return the lexical form of the variable."""
        return self.name


@dataclass(frozen=True)
class Constant(Term):
    """Concrete symbol (typically uppercase or numeric) that always evaluates to itself during unification."""

    symbol: Any

    def occurs(self, var_name: str) -> bool:
        """Constants never contain variables, so always return False."""
        return False

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        """Return the constant itself because substitutions do not change it."""
        return self

    def __str__(self) -> str:
        """Return the symbol as a string."""
        return str(self.symbol)


@dataclass(frozen=True)
class Function(Term):
    """Composite term consisting of a functor name and an ordered list of argument terms."""

    name: str
    arguments: List[Term]

    def occurs(self, var_name: str) -> bool:
        """Return True if any argument contains the variable `var_name`."""
        return any(arg.occurs(var_name) for arg in self.arguments)

    def apply_substitution(self, substitution: 'Substitution') -> 'Term':
        """Recursively apply `substitution` to every argument, returning a new function."""
        new_args = [arg.apply_substitution(
            substitution) for arg in self.arguments]
        return Function(self.name, new_args)

    def __str__(self) -> str:
        """Return the textual representation name(arg1, arg2, ...)."""
        if not self.arguments:
            return self.name
        return f"{self.name}(" + ", ".join(str(a) for a in self.arguments) + ")"
