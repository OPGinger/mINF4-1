from pathlib import Path


def path(filename) -> Path:
    """Gibt den absoluten Pfad zu einer Datei im Projektverzeichnis zurück.

    Funktioniert unabhängig vom Arbeitsverzeichnis und der verwendeten IDE,
    da der Pfad relativ zur Position dieses Moduls berechnet wird.

    Beispiel
    --------
    from utils.algo_path import path
    z = Array.from_file(path("data/seq0.txt"), ctx)
    """
    project_dir = Path(__file__).resolve().parent.parent
    return project_dir / filename


if __name__ == "__main__":
    filename = path("data/seq0.txt")
    print(filename)
    print(filename.resolve())
    print(filename.is_file())
    print(filename.exists())
