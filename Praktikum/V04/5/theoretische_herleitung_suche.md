# Task 5 - Theoretische Herleitung der Suchkosten

## Ziel
Herleitung der Anzahl der Vergleiche bei der erfolgreichen Suche in Abhaengigkeit von der Elementanzahl `n`.

## Modell fuer Vergleiche
Im verwendeten Suchcode wird pro besuchtem Knoten typischerweise zuerst `<` und danach `>` geprueft.
Dadurch gilt naeherungsweise:

`Vergleiche ~= 2 * (Anzahl besuchter Ebenen)`

Wenn ein Treffer in Tiefe `d` liegt (Wurzel hat Tiefe 0), dann:

`C(d) ~= 2 * (d + 1)`

Die Suchkosten sind damit proportional zur Tiefe bzw. zur Baumhoehe `h`.

---

## 1) Sortierter BST (entarteter Baum)

Bei sortiertem Einfuegen entsteht eine Kette mit Hoehe:

`h = n - 1`

Das `i`-te gefundene Element (in Kettenreihenfolge) kostet:

`C_i = 2i`

Gesamtkosten fuer die erfolgreiche Suche aller `n` Elemente genau einmal:

`C_total(n) = sum_{i=1..n} 2i = n(n+1)`

Durchschnittskosten pro Suche:

`C_avg(n) = C_total(n)/n = n + 1`

Asymptotisch:

`C_search(n) = Theta(n)`

Diese Formel erklaert exakt die gemessenen Werte:
- `n = 10  -> 10 * 11 = 110`
- `n = 100 -> 100 * 101 = 10100`
- `n = 500 -> 500 * 501 = 250500`

---

## 2) Zufaelliger BST

Bei zufaelliger Einfuegereihenfolge ist der Baum im Erwartungswert deutlich flacher.
Fuer erfolgreiche Suche gilt klassisch (Knotenzugriffe):

`E[Tiefe] ~= 2 ln(n)`

Mit etwa zwei Vergleichen pro Ebene folgt:

`E[C_search] ~= 4 ln(n) = Theta(log n)`

Fuer alle `n` erfolgreichen Suchen zusammen:

`C_total(n) = Theta(n log n)`

---

## 3) Sortierter AVL-Baum

Der AVL-Baum balanciert nach jedem Einfuegen. Daher bleibt die Hoehe logarithmisch:

`h = Theta(log n)`

Eine bekannte obere Schranke fuer AVL-Hoehe ist:

`h <= 1.44 * log2(n + 2) - 0.328`

Mit zwei Vergleichen pro Ebene ergibt sich fuer erfolgreiche Suche:

`C_search(n) <= 2 * (h + 1)`

also ebenfalls:

`C_search(n) = Theta(log n)`

und fuer alle `n` erfolgreichen Suchen:

`C_total(n) = Theta(n log n)`

---

## Fazit

- Sortierter BST: lineare Suche pro Anfrage (`Theta(n)`), quadratische Gesamtkosten fuer alle Schluessel (`Theta(n^2)`).
- Zufaelliger BST: logarithmische Suche im Erwartungswert (`Theta(log n)`), Gesamtkosten `Theta(n log n)`.
- Sortierter AVL: durch Balancierung ebenfalls logarithmische Suche (`Theta(log n)`), Gesamtkosten `Theta(n log n)`.

Die Messdaten aus `messwerte.csv` sind damit theoretisch konsistent.
