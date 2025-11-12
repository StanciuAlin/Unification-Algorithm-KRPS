import re

from src.models.literal import Literal
from src.models.term import Constant, Function, Term, Variable


class ParserAIMA:
    """
    Utility that classifies and parses strings into Term or Literal objects following the AIMA syntax rules.
        - Variables: lowercase letter (x, y, z)
        - Constants: uppercase letter (John, Mary, Dog)
        - Functions: lowercase letter followed by parentheses (f(x), g(x, y))
        - Predicates/Literals: uppercase letter followed by parentheses (Loves(John, x))
        - Negation: symbols ¬ or ~ (prefix)
    """

    @staticmethod
    def detect_type(expr: str) -> str:
        """Classify the expression as variable, constant, function, literal, or unknown."""
        expr = expr.strip()

        if expr.startswith(("¬", "~")):
            return "literal_negated"

        # Varible
        if re.fullmatch(r'[a-z]\w*', expr):
            return "variable"

        # Constant
        if re.fullmatch(r'[A-Z]\w*', expr):
            return "constant"

        # Functin or Literal
        match = re.match(r'([A-Za-z]\w*)\((.*)\)', expr)
        if match:
            name = match.group(1)
            if name[0].isupper():
                return "literal"  # AIMA: predicate/literal
            else:
                return "function"

        return "unknown"

    @staticmethod
    def _split_arguments(args_str: str):
        """Return a list of argument substrings while respecting nested parentheses."""
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

    @staticmethod
    def parse_term(text: str) -> Term:
        """Parse a textual representation into a `Term` instance (variable, constant, or function)."""
        text = text.strip()

        # Variable
        if re.fullmatch(r'[a-z]\w*', text):
            return Variable(text)

        # Constant (also numbers)
        elif re.fullmatch(r'[A-Z]\w*', text) or re.fullmatch(r'\d+', text):
            return Constant(text)

        # Function: lowercase letter followed by parentheses
        match = re.match(r'([a-z]\w*)\((.*)\)', text)
        if match:
            name, args_str = match.groups()
            args = [ParserAIMA.parse_term(
                arg) for arg in ParserAIMA._split_arguments(args_str)]
            return Function(name, args)

        raise ValueError(f"Invalid term format (AIMA): {text}")

    @staticmethod
    def parse_literal(text: str) -> Literal:
        """Parse a predicate string (optionally negated) into a `Literal`."""
        text = text.strip()
        negated = False

        # Find out negation
        if text.startswith(("¬", "~")):
            negated = True
            text = text[1:].strip()

        # Predicate: uppercase letter followed by parentheses
        match = re.match(r'([A-Z]\w*)\((.*)\)', text)
        if not match:
            raise ValueError(f"Invalid literal format (AIMA): {text}")

        name, args_str = match.groups()
        args = [ParserAIMA.parse_term(arg)
                for arg in ParserAIMA._split_arguments(args_str)]
        return Literal(name, args, negated)

    @staticmethod
    def parse_expression(text: str):
        """Auto-detect expression type and parse it as either a literal or term."""
        kind = ParserAIMA.detect_type(text)
        if kind in {"literal", "literal_negated"}:
            return ParserAIMA.parse_literal(text)
        elif kind in {"variable", "constant", "function"}:
            return ParserAIMA.parse_term(text)
        else:
            raise ValueError(f"Cannot determine expression type: {text}")
