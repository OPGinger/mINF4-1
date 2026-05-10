# Task 3 - Degeneration of BST

## Goal
Show BST degeneration by inserting sorted values and analyzing the resulting height.

## Method
- Build one tree with ascending insertion `1..n`.
- Build one tree with descending insertion `n..1`.
- Export both trees as Graphviz PDFs.
- Compare heights.

## Files
- `aufgabe3_entartung_bst.py`: implementation.
- `antworten.txt`: measured values and interpretation.
- `BST_Degeneration_Ascending_*.gv.pdf`: ascending case.
- `BST_Degeneration_Descending_*.gv.pdf`: descending case.

## Run
From this folder:

```powershell
& "../../.venv/Scripts/python.exe" "aufgabe3_entartung_bst.py"
```
