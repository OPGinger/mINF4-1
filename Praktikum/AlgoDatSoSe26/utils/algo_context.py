import matplotlib.pyplot as plt


class AlgoContext:
    """
    Kontext für die Instrumentierung von Algorithmen.

    Jeder Algorithmus erhält eine eigene Instanz – kein globaler Zustand.
    Die Zähler werden von Int- und Array-Operationen automatisch erhöht.

    Zähler
    ------
    reads           Lesezugriffe (bei Vergleichen und Arithmetik je Operand)
    writes          Schreibzugriffe (set, Zuweisung, augmented assignment)
    comparisons     Vergleiche  (<, <=, >, >=, ==, !=)
    additions       Additionen  (+, +=)
    subtractions    Subtraktionen  (-, -=)
    multiplications Multiplikationen  (*, *=)
    divisions       Divisionen  (/, //, %, /=, //=)
    bitops          Bitoperationen  (&, |, ^, <<, >>)

    Beispiel
    --------
    ctx = AlgoContext()
    z = Array.random(20, -100, 100, ctx)
    bubble_sort(z, ctx)
    print(ctx)
    ctx.save_stats(20)
    """

    def __init__(self):
        self.reads = 0
        self.writes = 0
        self.comparisons = 0
        self.additions = 0
        self.subtractions = 0
        self.multiplications = 0
        self.divisions = 0
        self.bitops = 0
        self._stats: dict[int, dict] = {}

    def reset(self):
        """Setzt alle Zähler auf 0 zurück."""
        self.reads = 0
        self.writes = 0
        self.comparisons = 0
        self.additions = 0
        self.subtractions = 0
        self.multiplications = 0
        self.divisions = 0
        self.bitops = 0

    def _snapshot(self) -> dict:
        return {
            "reads":           self.reads,
            "writes":          self.writes,
            "comparisons":     self.comparisons,
            "additions":       self.additions,
            "subtractions":    self.subtractions,
            "multiplications": self.multiplications,
            "divisions":       self.divisions,
            "bitops":          self.bitops,
        }

    def save_stats(self, n: int):
        """Speichert einen Schnappschuss der aktuellen Zähler für Eingabegröße n."""
        self._stats[n] = self._snapshot()

    def plot_stats(self, labels: list[str]):
        """
        Zeichnet die gespeicherten Statistiken als Liniendiagramm.

        Parameters
        ----------
        labels : list[str]
            Zähler-Namen, z.B. ["comparisons", "writes"]
        """
        data = self._stats
        x = list(data.keys())

        fig, axes = plt.subplots(len(labels), 1, figsize=(8, 4 * len(labels)), sharex=True)
        if len(labels) == 1:
            axes = [axes]

        for ax, label in zip(axes, labels):
            y = [data[k][label] for k in x]
            ax.plot(x, y, label=label)
            ax.set_ylabel(label)
            ax.legend()

        plt.xlabel("n")
        plt.tight_layout()
        plt.show()

    def summary(self) -> str:
        """Gibt alle Zähler als formatierten Text zurück."""
        return (
            f"Reads:           {self.reads}\n"
            f"Writes:          {self.writes}\n"
            f"Comparisons:     {self.comparisons}\n"
            f"Additions:       {self.additions}\n"
            f"Subtractions:    {self.subtractions}\n"
            f"Multiplications: {self.multiplications}\n"
            f"Divisions:       {self.divisions}\n"
            f"Bitwise ops:     {self.bitops}"
        )

    def __str__(self):
        return self.summary()

    def __repr__(self):
        return (f"AlgoContext(reads={self.reads}, writes={self.writes}, "
                f"comparisons={self.comparisons})")


class _NullContext:
    """
    Kontext der alle Operationen stillschweigend ignoriert.

    Wird intern von Range() verwendet, damit Schleifenindex-Arithmetik
    standardmäßig nicht mitgezählt wird.

    __setattr__ ist absichtlich ein no-op: ``ctx.reads += 1`` bleibt wirkungslos.
    """
    reads = writes = comparisons = 0
    additions = subtractions = multiplications = divisions = bitops = 0

    def __setattr__(self, name, value):
        pass  # alle Schreibzugriffe ignorieren

    def save_stats(self, n): pass
    def reset(self): pass


NULL_CTX = _NullContext()
