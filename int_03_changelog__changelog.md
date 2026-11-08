# Verlauf 3d-druck

**ID:** changelog

**Stand:** 08.11.2026 – append-only (`std_00_workflow`, `changelog-principle`). Stufe 1.

---

## 2026-11-08

**Projekt angelegt und erster Ablauf dokumentiert.** Das Rasierer-Gehäuse (Haube und Deckel) wurde im Chat entworfen: erst als zylindrische Form mit Flansch, dann als nahtlose Birnenform. Das Blender-Skript lief auf Blender 5.2.3, der STL-Export und das Slicen mit Cura 5.12.0 für den Anycubic i3 Mega funktionierten. Der Drucker liest keinen STL, sondern nur G-Code vom Slicer (`workflow-claude-blender-cura`, `error-patterns`). Anlass: Der Ablauf soll ohne den Chatverlauf wiederholbar sein. Teil: `shaver-housing`.

**Ordnerstruktur des Repositories festgelegt.** Dokumente (`int_*`) liegen im Hauptverzeichnis, Anhänge unter `parts/<teil>/<version>/` (Skript, `stl/`, `gcode/`), Cura-Profile unter `profiles/cura/`. Anlass: Skripte, STL und G-Code gehören zu Versionen eines Teils und sollen mit ihm zusammenbleiben. Register: `registry`, `assets`.

**Projekt 3D-Lab und Aufteilung auf zwei Repositories.** Das claude.ai-Projekt für 3D-Themen heißt 3D-Lab. Es führt die Druckmodelle hier und die 3D-Komponente für Tenants in `vertilus-docs` und `knowledge-docs` (`project`, `repository-split`). Ordner `profiles/cura/` angelegt, das Profil des ersten Slicens bleibt draußen, weil die Einstellungen nicht stimmten. Anlass: Entscheidung des Betreibers im Chat.
