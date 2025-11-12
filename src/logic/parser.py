import re
from src.models.term import Variable, Constant, Function, Term
from src.models.literal import Literal


class ParserAIMA:
    """
    Parse according to AIMA (Russell & Norvig) conventions:
    - Variables: lowercase letter (x, y, z)
    - Constants: uppercase letter (John, Mary, Dog)
    - Functions: lowercase letter followed by parentheses (f(x), g(x, y))
    - Predicates/Literals: uppercase letter followed by parentheses (Loves(John, x))
    - Negation: symbols ¬ or ~ (prefix)
    """

    # Find out type of expression
    @staticmethod
    def detect_type(expr: str) -> str:
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

    # Split arguments respecting nested parentheses
    @staticmethod
    def _split_arguments(args_str: str):
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

    # Parse TERM (Variable, Constant, Function)
    @staticmethod
    def parse_term(text: str) -> Term:
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

    # Parse LITERAL (Predicate, possibly negated)
    @staticmethod
    def parse_literal(text: str) -> Literal:
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

    # Auto-detect and parse expression (Term or Literal)
    @staticmethod
    def parse_expression(text: str):
        kind = ParserAIMA.detect_type(text)
        if kind in {"literal", "literal_negated"}:
            return ParserAIMA.parse_literal(text)
        elif kind in {"variable", "constant", "function"}:
            return ParserAIMA.parse_term(text)
        else:
            raise ValueError(f"Cannot determine expression type: {text}")
