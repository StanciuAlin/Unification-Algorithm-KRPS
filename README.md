# Unification Algorithm Project
## 1. Goal
The goal of this project is to implement the unification algorithm for first-order logic (FOL), test it on several examples, and show how it can be integrated in a small resolution-style component. The project is structured using clean code and SOLID principles.

## 2. Architecture
- `src/models/term.py` – Term hierarchy: `Term`, `Variable`, `Constant`, `Function`
- `src/models/errors.py` - Custom exception raised when unification fails
- `src/logic/substitution.py` – `Substitution` class, represents a mapping from variable names to terms.
- `src/logic/unifier.py` – `Unifier` class implementing the unification algorithm for FOL terms
- `src/logic/resolution.py` – a simple resolution helper and `Literal` class to show how unification is used in resolution.
- `src/utils/printer.py` - a simple function to print a header at the starting point of the program execution
- `tests/test_unification.py` – 17 test cases
- `main.py` – entry point

## 3. Design Notes
- **Single Responsibility**: each class has a single reason to change.
- **Open/Closed**: new term types can be added in `models` without changing the unifier logic.
- **Clean Code**: descriptive names, small functions, no hard-coded data in logic modules.
- **Separation of Concerns**: models vs logic vs tests.

## 4. Running
```bash
python3 main.py
```
This will execute the 10 predefined tests and print the resulting substitutions.

## 5. Tests Covered
1. Variable with constant
2. Variable with variable
3. Equal constants
4. Different constants (expected failure)
5. Functions with 1 argument
6. Functions with 2 arguments
7. Nested functions
8. Occurs-check failure
9. Predicate-style terms
10. Resolution-style literal unification

## 6. Integration with Resolution
The file `src/logic/resolution.py` shows how unification is normally consumed by a resolution algorithm: two complementary literals are unified, and the resulting substitution can then be applied to the parent clauses.
