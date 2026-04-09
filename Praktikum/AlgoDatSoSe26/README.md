# Algorithmen und Datenstrukturen – SoSe 26

Dieses Repository enthält den Code zur Vorlesung. Neben den Vorlesungsbeispielen
bietet es ein kleines Framework, mit dem ihr eure eigenen Algorithmen
**automatisch auf Operationen messen** könnt – ohne den Algorithmus selbst
anfassen zu müssen.

---

## Wozu das Framework?

In der Vorlesung analysieren wir Algorithmen theoretisch mit der O-Notation.
Das Framework erlaubt euch, diese Theorie **empirisch zu überprüfen**: Ihr
implementiert euren Algorithmus genauso wie in Python üblich – nur dass ihr
statt `list` und `int` die Wrapper-Typen `Array` und `Int` verwendet. Das
Framework zählt dann im Hintergrund automatisch Vergleiche, Lese- und
Schreibzugriffe sowie arithmetische Operationen.

---

## Schnellstart

### 1. Kontext anlegen

```python
from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_range import Range

ctx = AlgoContext()
```

`AlgoContext` ist der Zähler. Ihr legt ihn einmal an und gebt ihn an eure
Datenstrukturen weiter.

### 2. Array befüllen

```python
z = Array.random(10, -100, 100, ctx)   # 10 Zufallszahlen zwischen -100 und 100
# oder:
z = Array([5, 3, 8, 1, 9, 2], ctx)    # eigene Werte
```

### 3. Algorithmus schreiben

Schreibt euren Algorithmus wie gewohnt. `Range` ist ein Drop-in-Ersatz für
`range` und liefert ebenfalls `Int`-Objekte – allerdings ohne Verbindung zum
Zähler. Dadurch wird **Indexarithmetik** (`j - 1`, `i + 1`) nicht mitgezählt,
während Operationen auf Array-*Inhalten* (die ja den echten `ctx` tragen) weiterhin
erfasst werden. Das entspricht der üblichen Konvention: gezählt werden nur
Operationen auf den Daten, nicht die Schleifensteuerung.

```python
def insertion_sort(z: Array, ctx: AlgoContext):
    for i in Range(1, len(z)):
        elem = z[i]                     # liest z[i] (1 Lesezugriff)
        j = int(i) - 1
        while j >= 0 and z[j] > elem:  # vergleicht (1 Vergleich pro Schritt)
            z[j + 1] = z[j]            # schreibt (1 Schreibzugriff)
            j -= 1
        z[j + 1] = elem
```

### 4. Ausführen und Ergebnis ablesen

```python
insertion_sort(z, ctx)

print(ctx.comparisons)   # Anzahl Vergleiche
print(ctx.reads)         # Lesezugriffe
print(ctx.writes)        # Schreibzugriffe
print(ctx.additions)     # Additionen
```

Oder kompakt:

```python
print(ctx.summary())
```

### 5. Komplexität über mehrere Eingabegrößen plotten

```python
def analyze(sort_func, sizes):
    ctx = AlgoContext()
    for size in sizes:
        ctx.reset()
        z = Array.random(size, -100, 100, ctx)
        sort_func(z, ctx)
        ctx.save_stats(size)
    ctx.plot_stats(["comparisons", "writes"])

analyze(insertion_sort, range(10, 201, 10))
```

Das öffnet ein Matplotlib-Fenster mit dem Verlauf der gezählten Operationen
über die Eingabegröße – ihr seht direkt, ob euer Algorithmus z.B. quadratisch oder
linear wächst.

---

## Verfügbare Zähler

| Attribut        | Was wird gezählt                          |
|-----------------|-------------------------------------------|
| `comparisons`   | `<`, `>`, `<=`, `>=`, `==`, `!=`          |
| `reads`         | Lesezugriffe auf `Int`-Werte              |
| `writes`        | Schreibzugriffe (Zuweisung, `swap`)       |
| `additions`     | `+`, `+=`                                 |
| `subtractions`  | `-`, `-=`                                 |
| `multiplications` | `*`, `*=`                               |
| `divisions`     | `/`, `//`, `/=`                           |
| `bitops`        | `&`, `\|`, `^`, `<<`, `>>`               |

---

## Struktur des Repositories

```
utils/          Framework-Dateien (AlgoContext, Int, Array, Range)
vorlesung/      Vorlesungsbeispiele, geordnet nach Lektionsnummer
praktika/       Aufgabenstellungen der Praktika
playground/     Eure eigenen Abgaben und Experimente
data/           Beispieldatensätze
```

Die Vorlesungsbeispiele in `vorlesung/` sind vollständig mit dem Framework
instrumentiert und können als Vorlage für eigene Implementierungen dienen.

## Datenpfade

Die Demodaten in `data/` werden über `path()` aus `utils.algo_path` adressiert.
Die Funktion liefert immer den absoluten Pfad relativ zum Projektverzeichnis –
unabhängig davon, aus welchem Verzeichnis ihr das Skript startet oder welche IDE
ihr verwendet:

```python
from utils.algo_path import path

z = Array.from_file(path("data/seq0.txt"), ctx)
```

## PriorityQueue

Für Graphalgorithmen (z.B. Dijkstra) steht eine fertige `PriorityQueue` bereit.
Sie basiert intern auf einem Heap – das Prinzip habt ihr in der Vorlesung zu
Heap Sort kennengelernt. Als Abkürzung dürft ihr die fertige Klasse verwenden:

```python
from utils.algo_priority_queue import PriorityQueue

pq = PriorityQueue()
pq.add_or_update("A", 0)    # Knoten mit Priorität (Distanz) eintragen
pq.add_or_update("B", 5)
pq.add_or_update("B", 2)    # Priorität aktualisieren
node, dist = pq.pop()       # liefert ("A", 0)
```
