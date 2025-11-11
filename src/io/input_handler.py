# src/io/input_handler.py
from src.models.term import Term, Variable, Function
from src.models.literal import Literal
from src.models.clause import Clause
from src.models.errors import InputError


class InputHandler:
    def __init__(self):
        print("🧩 Knowledge Representation CLI")
        print("Introduceți expresii logice în format natural (ex: P(a,b) ∧ ¬Q(x))")
        print("Scrieți 'exit' pentru a ieși.\n")

    def read_input(self) -> str:
        """Citește linia de input de la user și face validări simple."""
        user_input = input(">>> ").strip()
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("La revedere! 👋")
            exit(0)
        if not user_input:
            raise InputError("Input gol. Introdu o expresie logică validă.")
        return user_input

    def parse_expression(self, text: str):
        """Transformă textul într-o structură logică (Term, Literal, Clause)."""
        # Poți integra aici parserul tău de string (pe care l-ai menționat anterior)
        # Ex: detectează predicatul, argumentele, negarea etc.
        try:
            if "∧" in text or "∨" in text:
                # Parsează o propoziție complexă
                return Clause.from_string(text)
            elif "(" in text:
                return Literal.from_string(text)
            else:
                return Term.from_string(text)
        except Exception as e:
            raise InputError(f"Eroare la interpretarea expresiei: {e}")
