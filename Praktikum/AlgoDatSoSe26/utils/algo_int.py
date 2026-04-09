from __future__ import annotations
from utils.algo_context import AlgoContext, _NullContext, NULL_CTX


class Int:
    """
    Instrumentierter Integer-Typ.

    Alle Operationen werden im zugehörigen AlgoContext gezählt.
    Der Rohwert ist über das Attribut ``value`` direkt lesbar (kein Zähler),
    was für Visualisierungen benötigt wird.

    Zählregeln
    ----------
    Vergleich  (a < b):   2 reads + 1 comparison
    Arithmetik (a + b):   2 reads + 1 arithmetische Operation → neues Int
    Augmented  (a += b):  2 reads + 1 arithmetische Operation + 1 write
    set(v):               1 write  (+1 read falls v ein Int ist)

    Auto-Wrapping
    -------------
    Alle Operatoren akzeptieren auch plain-Python-Werte (int, float).
    Diese werden intern zu Int(v, NULL_CTX) gewrappt, ohne Zähler zu erhöhen.

    Beispiel
    --------
    ctx = AlgoContext()
    a = Int(5, ctx)
    b = Int(3, ctx)
    if a > b:          # 2 reads, 1 comparison
        a += b         # 2 reads, 1 addition, 1 write
    print(a.value)     # 8  (kein Zähler)
    """

    def __init__(self, value, ctx: AlgoContext | _NullContext = NULL_CTX):
        if isinstance(value, Int):
            self._value = value._value
        else:
            self._value = value
        self._ctx = ctx

    # ------------------------------------------------------------------
    # Rohwert-Zugriff (für Visualisierung, kein Zähler)
    # ------------------------------------------------------------------

    @property
    def value(self):
        """Rohwert für Visualisierung – wird nicht gezählt."""
        return self._value

    # ------------------------------------------------------------------
    # Schreiben
    # ------------------------------------------------------------------

    def set(self, new_value):
        """
        Setzt den Wert.

        Zählt: 1 write  (+1 read falls new_value ein Int ist)
        """
        self._ctx.writes += 1
        if isinstance(new_value, Int):
            self._ctx.reads += 1
            self._value = new_value._value
        else:
            self._value = new_value

    # ------------------------------------------------------------------
    # Interner Hilfshelfer
    # ------------------------------------------------------------------

    def _wrap(self, other) -> Int:
        """Wraps plain Python-Wert zu Int mit NULL_CTX (kein Zähler)."""
        if isinstance(other, Int):
            return other
        return Int(other, NULL_CTX)

    # ------------------------------------------------------------------
    # Vergleiche  (2 reads + 1 comparison je Operation)
    # ------------------------------------------------------------------

    def __eq__(self, other):
        if other is None:
            return False
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.comparisons += 1
        return self._value == other._value

    def __ne__(self, other):
        if other is None:
            return True
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.comparisons += 1
        return self._value != other._value

    def __lt__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.comparisons += 1
        return self._value < other._value

    def __le__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.comparisons += 1
        return self._value <= other._value

    def __gt__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.comparisons += 1
        return self._value > other._value

    def __ge__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.comparisons += 1
        return self._value >= other._value

    # ------------------------------------------------------------------
    # Arithmetik  (2 reads + 1 op → neues Int mit gleichem ctx)
    # ------------------------------------------------------------------

    def __add__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.additions += 1
        return Int(self._value + other._value, self._ctx)

    def __radd__(self, other):
        return self._wrap(other).__add__(self)

    def __sub__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.subtractions += 1
        return Int(self._value - other._value, self._ctx)

    def __rsub__(self, other):
        return self._wrap(other).__sub__(self)

    def __mul__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.multiplications += 1
        return Int(self._value * other._value, self._ctx)

    def __rmul__(self, other):
        return self._wrap(other).__mul__(self)

    def __truediv__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.divisions += 1
        return Int(self._value / other._value, self._ctx)

    def __floordiv__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.divisions += 1
        return Int(self._value // other._value, self._ctx)

    def __mod__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.divisions += 1
        return Int(self._value % other._value, self._ctx)

    # ------------------------------------------------------------------
    # Augmented assignment  (2 reads + 1 op + 1 write, in-place)
    # ------------------------------------------------------------------

    def __iadd__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.additions += 1
        self._ctx.writes += 1
        self._value += other._value
        return self

    def __isub__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.subtractions += 1
        self._ctx.writes += 1
        self._value -= other._value
        return self

    def __imul__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.multiplications += 1
        self._ctx.writes += 1
        self._value *= other._value
        return self

    def __itruediv__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.divisions += 1
        self._ctx.writes += 1
        self._value /= other._value
        return self

    def __ifloordiv__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.divisions += 1
        self._ctx.writes += 1
        self._value //= other._value
        return self

    def __imod__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.divisions += 1
        self._ctx.writes += 1
        self._value %= other._value
        return self

    # ------------------------------------------------------------------
    # Bitoperationen  (2 reads + 1 bitop + 1 write für in-place)
    # ------------------------------------------------------------------

    def __and__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        return Int(self._value & other._value, self._ctx)

    def __or__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        return Int(self._value | other._value, self._ctx)

    def __xor__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        return Int(self._value ^ other._value, self._ctx)

    def __lshift__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        return Int(self._value << other._value, self._ctx)

    def __rshift__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        return Int(self._value >> other._value, self._ctx)

    def __iand__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        self._ctx.writes += 1
        self._value &= other._value
        return self

    def __ior__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        self._ctx.writes += 1
        self._value |= other._value
        return self

    def __ixor__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        self._ctx.writes += 1
        self._value ^= other._value
        return self

    def __ilshift__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        self._ctx.writes += 1
        self._value <<= other._value
        return self

    def __irshift__(self, other):
        other = self._wrap(other)
        self._ctx.reads += 2
        self._ctx.bitops += 1
        self._ctx.writes += 1
        self._value >>= other._value
        return self

    # ------------------------------------------------------------------
    # Typkonvertierung und Darstellung
    # ------------------------------------------------------------------

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def __index__(self):
        """Ermöglicht Verwendung als Listen-Index (z.B. arr[i])."""
        return int(self._value)

    def __hash__(self):
        return hash(self._value)

    def __bool__(self):
        return bool(self._value)

    def __neg__(self):
        return Int(-self._value, self._ctx)

    def __abs__(self):
        return Int(abs(self._value), self._ctx)

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"Int({self._value})"
