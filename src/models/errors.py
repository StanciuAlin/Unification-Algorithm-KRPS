class UnificationError(Exception):
    """Exception capturing the reason and optional offending terms when unification cannot proceed."""

    def __init__(self, message: str, t1=None, t2=None):
        """
        Parameters:
        - message: custom error message
        - t1, t2: optional terms involved in the unification failure
        """
        self.message = message
        self.t1 = t1
        self.t2 = t2
        super().__init__(self.message)

    def __str__(self):
        """Return a string representation of the error."""
        base = self.message
        if self.t1 is not None and self.t2 is not None:
            base += f" | Terms: {self.t1}, {self.t2}"
        return base


class InputError(Exception):
    """Exception raised for malformed CLI inputs before parsing or unification takes place."""

    def __init__(self, message="Error in input handling"):
        """Initialize input error with a helpful message."""
        super().__init__(message)
