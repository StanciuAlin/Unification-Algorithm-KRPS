class UnificationError(Exception):
    """Custom exception raised when unification fails."""

    def __init__(self, message: str, t1=None, t2=None):
        """
        Parameters:
        - message: mesajul personalizat de eroare
        - t1, t2: termeni opționali implicați în eroare (pentru context)
        """
        self.message = message
        self.t1 = t1
        self.t2 = t2
        super().__init__(self.message)

    def __str__(self):
        """Returnează mesajul clar, eventual cu termenii incluși."""
        base = self.message
        if self.t1 is not None and self.t2 is not None:
            base += f" | Terms: {self.t1}, {self.t2}"
        return base
