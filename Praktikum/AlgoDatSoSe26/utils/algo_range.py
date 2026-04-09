from __future__ import annotations
from utils.algo_context import AlgoContext, NULL_CTX
from utils.algo_int import Int


def Range(start_or_stop, stop=None, step: int = 1, ctx: AlgoContext = None):
    """
    Drop-in Ersatz für range(), der Int-Objekte zurückgibt.

    Wird wie Pythons range() aufgerufen:
        Range(stop)
        Range(start, stop)
        Range(start, stop, step)

    Indexarithmetik und Zählung
    ---------------------------
    Ohne ctx-Argument (Standard) erhalten die erzeugten Indices einen NULL_CTX –
    Arithmetik auf Loop-Indices (z.B. ``j - 1``) wird dann **nicht** gezählt.
    Das entspricht dem üblichen Lehrbuchwunsch: nur Operationen auf Array-Inhalten
    sollen in die Komplexitätsanalyse einfließen.

    Mit ctx-Argument werden auch Indexoperationen gezählt:
        for j in Range(n, ctx=ctx): ...

    Beispiel
    --------
    ctx = AlgoContext()
    z = Array.random(10, 0, 99, ctx)
    for i in Range(len(z) - 1):      # i ist Int, Arithmetik nicht gezählt
        if z[i] > z[i + 1]:           # Vergleich gezählt (z-Zellen haben ctx)
            z.swap(i, i + 1)
    """
    _ctx = ctx if ctx is not None else NULL_CTX

    if stop is None:
        start, stop_ = 0, int(start_or_stop)
    else:
        start, stop_ = int(start_or_stop), int(stop)
    step = int(step)

    assert step != 0, "Range: step darf nicht 0 sein"

    num = start
    if step > 0:
        while num < stop_:
            yield Int(num, _ctx)
            num += step
    else:
        while num > stop_:
            yield Int(num, _ctx)
            num += step
