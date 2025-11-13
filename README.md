# Unification Algorithm Project

## 1. Goal

Implement and demonstrate the Most General Unifier (MGU) computation for first-order logic (FOL) terms and literals using the AIMA (Russell & Norvig) notation.  
The application provides:

- A reusable Python module that performs unification with occurs-check protection.
- A small resolution helper that shows how literal unification is consumed in inference.
- A CLI experience that guides the user through term/literal unification exercises or runs the bundled test suite.

## 2. Architecture

| Layer                       | Description                                                                                                       |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `src/models/term.py`        | Defines the `Term` abstraction plus concrete `Variable`, `Constant`, and `Function` nodes with parsing helpers.   |
| `src/models/literal.py`     | Predicate/literal representation with negation handling, equality helpers, and parsing.                           |
| `src/models/errors.py`      | Domain-specific exceptions (`UnificationError`, `InputError`) with contextual metadata.                           |
| `src/logic/substitution.py` | Immutable substitution objects that apply mappings, compose, and pretty-print in AIMA style.                      |
| `src/logic/unifier.py`      | Core unification algorithm for terms and complementary literals, including occurs-check and verbose tracing.      |
| `src/logic/parser.py`       | String-to-structure parser aligned with AIMA conventions and used by both CLI and tests.                          |
| `src/logic/resolution.py`   | Minimal resolution scaffold that unifies complementary literals to showcase integration.                          |
| `src/io/input_handler.py`   | CLI controller that validates input, auto-detects modes, and orchestrates prompts or automated tests.             |
| `src/utils/printer.py`      | Shared, colorized CLI output helpers (headers, menus, notifications).                                             |
| `tests/test_unification.py` | Demonstrative regression suite covering successful and failing unification scenarios.                             |
| `main.py`                   | Interactive entry point that exposes menu-based workflows for terms, literals, auto-detect, or running all tests. |

## 3. Design Notes

### AIMA Conventions in Code

The program mirrors the casing and notation from _Artificial Intelligence: A Modern Approach (4e)_ so students can type expressions exactly as shown in the textbook.

| Concept             | Syntax in this project          | Example inputs                   | Parsed into                 |
| ------------------- | ------------------------------- | -------------------------------- | --------------------------- |
| Variable            | Lowercase identifiers           | `x`, `child`, `temp1`            | `Variable("x")`             |
| Constant / Name     | Uppercase identifiers or digits | `John`, `A`, `42`                | `Constant("John")`          |
| Function term       | Lowercase functor + parentheses | `parent(x, y)`, `loves(john, X)` | `Function("parent", [...])` |
| Predicate / Literal | Uppercase functor + parentheses | `Loves(John, x)`                 | `Literal("Loves", [...])`   |
| Negation            | Prefix `¬` (preferred) or `~`   | `¬Loves(John, x)`, `~Animal(y)`  | Literal with `negated=True` |

Key implications:

1. **Parser-driven detection:** `ParserAIMA.detect_type` uses these casing rules to distinguish terms from literals automatically.
2. **Consistency across CLI/tests:** prompts, examples, and assertions all reuse the same convention, so there is no mismatch between documentation and behavior.
3. **Occurs-check clarity:** because variables are always lowercase, the occurs-check quickly identifies self-referential substitutions like `x / f(x)`.
4. **Notation convention used:** the substitution `{ a / X }` means “replace the variable `a` with the constant `X`.” This is the inverse display order of the classic AIMA notation `{ X / a }`, but both convey the exact same mapping.

### Clean Architecture Principles

- **Single Responsibility:** parsing, term modeling, substitutions, unification, I/O, and presentation each live in dedicated modules.
- **Open/Closed:** add new term kinds or output styles without changing the unifier core.
- **Explicit Errors:** domain errors include the failing terms so the CLI can display meaningful diagnostics.
- **Testability:** most modules are framework-independent and exercised via `tests/test_unification.py`.

## 4. Features

1. **Term & Literal Unification:** Computes MGUs while guarding against occurs-check violations.
2. **Literal Complement Detection:** Confirms complementary predicates before attempting literal unification.
3. **CLI Modes:** Term unification, literal unification, auto-detected mode, or built-in regression tests.
4. **Parser Utilities:** Convert free-form user input to structured terms/literals.
5. **Resolution Demo:** Shows how substitutions produced by unification plug into a resolution step.
6. **Rich CLI Output:** Colorized messaging guides the user through each operation.

## 5. Running

```bash
python3 main.py
```

Steps performed by the CLI:

1. Displays AIMA conventions and the main menu.
2. Lets the user choose between term mode, literal mode, auto-detect, running the predefined tests, or exiting.
3. After unification, prints either the MGU or the reason unification failed, then offers to continue or exit.

### CLI Flows & Sample Runs

#### Option 1 – Term unification

```text
Mode: Term Unification
Write the first term/expression: king(X)
Write the second term/expression: king(john)
⚙️  Running Unification Algorithm for 'king(X)' and 'king(john)' ...
Most General Unifier (MGU): { john / X }
```

_Error example_

```text
Mode: Term Unification
Write the first term/expression: X
Write the second term/expression: f(X)
⚙️  Running Unification Algorithm for 'X' and 'f(X)' ...
Unification Error: Occurs check failed: variable 'X' occurs in term 'f(X)'
```

#### Option 2 – Literal unification

```text
Mode: Literal Unification
Write the first term/expression: Loves(sarah, Y)
Write the second term/expression: ~Loves(sarah, chocolate)
⚙️  Running Unification Algorithm for 'Loves(sarah, Y)' and '~Loves(sarah, chocolate)' ...
Literals unified successfully: { chocolate / Y }
```

_Error example_

```text
Mode: Literal Unification
Write the first term/expression: P(X, a)
Write the second term/expression: P(b, a)
⚙️  Running Unification Algorithm for 'P(X, a)' and 'P(b, a)' ...
Unification Error: Literals P(X, a) and P(b, a) are not complementary
```

#### Option 3 – Auto-detect (term vs literal)

```text
Mode automatically detected → Term
Write the first term/expression: parent(john, X)
Write the second term/expression: parent(john, mary)
⚙️  Running Unification Algorithm for 'parent(john, X)' and 'parent(john, mary)' ...
Most General Unifier (MGU): { mary / X }
```

#### Option 4 – Run bundled regression tests

```text
⚙️  Running predefined unification tests ...
[01] X  |  a
    Result: { a / X }
    Expected: { a / X }
...
Test Summary
Term tests passed: 10/10
Literal tests passed: 7/7
Total passed: 17/17 (100%)
```

## 6. Tests

### Quick Smoke (from CLI)

Choose option `4` (“Run predefined tests”) when executing `python3 main.py`. The suite prints each test case, the resulting substitution, and expected output.

### Automated (via pytest)

```bash
python3 -m pytest tests/test_unification.py
```

The file covers:

- Successful term unifications (variables vs constants, nesting, repeated variables).
- Expected failures (occurs-check, arity mismatches, incompatible functors).
- Literal unifications, including complement detection and substitution propagation.

## 7. Integration with Resolution

`src/logic/resolution.py` demonstrates how the `Unifier` is used inside a resolution step:

1. Validate that two literals are complementary.
2. Compute their unifier via the shared `Unifier`.
3. Return the resulting substitution so the caller can resolve the parent clauses.

## 8. Future Enhancements

- GUI/Web UI for interactive unification trees and proof steps.
- CNF pipeline and a full resolution loop.
- Support for additional syntax sugar (e.g., infix operators or quantifiers).
- Standardizing apart & variable renaming across clauses.
- Richer CLI history / logging and optional batch mode for automated grading.
- Performance: occurs-check variants, benchmarking.

