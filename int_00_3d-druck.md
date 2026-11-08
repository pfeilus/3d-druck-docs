# Projektdatei 3d-druck

**ID:** project

**Stand:** 08.11.2026 – Entwurf zur Freigabe. Stabiler Teil, ändert sich nur bei grundsätzlichen Änderungen der Arbeitsweise. Liegt als `int_00_3d-druck.md` im Repository `pfeilus/3d-druck-docs` (Branch `main`, führende Fassung). Stufe 2 (nach Freigabe).

**Basiert auf `std_00_workflow`, Version `[OFFEN – beim Einrichten die aktuelle Version aus dem Master eintragen]`.** Genutzte Module (Kopien im claude.ai-Projekt): `std_05_github-setup`, `std_20_dokumentation` (Klasse Runbook), `std_90_project-template`. Projekttyp nach `module-matrix`: Bastelprojekt (eigen). Diese Datei enthält nur die 3d-druck-spezifischen Ergänzungen.

**Hinweis zu Abschnitts-IDs:** kebab-case, Englisch, Inhalt Deutsch (siehe `std_00_workflow`, `markdown-conventions`).

---

## project-overview {#project-overview}

Privates Projekt: Teile für den 3D-Druck werden im Chat mit Claude entworfen. Claude liefert ein Python-Skript, Blender erzeugt daraus das Modell, ein STL geht nach Cura, der G-Code auf den Drucker. Das Projekt hält den Arbeitsablauf (`workflow-claude-blender-cura`), die Skripte und die Daten der einzelnen Teile fest. Erstes Teil: Rasierer-Gehäuse (`shaver-housing`).

Das claude.ai-Projekt heißt **3D-Lab** und liest dieses Repository. Es behandelt zwei Themen: die Druckmodelle (hier dokumentiert) und die Entwicklung einer 3D-Komponente für einen vertilus-Tenant. Das zweite Thema wird bewusst in den vertilus-Repositories geführt (Option „ein Projekt, zwei Repositories“, Entscheidung 08.11.2026), siehe `repository-split`.

Ausrüstung: Drucker Anycubic i3 Mega (Bauraum 210 × 210 × 205 mm), Filament PLA Basic 1,75 mm schwarz, Blender 5.2.3, Ultimaker Cura 5.12.0, Shapr3D (Basic, kein STEP-Export) für Zeichnungen.

## role-and-scope {#role-and-scope}

Du unterstützt Entwurf und Dokumentation von 3D-Druck-Teilen: Skripte für Blender liefern und vor der Übergabe headless testen, Maße und Entscheidungen festhalten, den Ablauf aktuell halten.

Ausdrücklich nicht Teil dieses Projekts:
- Inhalte zur 3D-Komponente für Tenants (Vision, Backlog, Machbarkeit, Werkzeugsteckbriefe). Sie gehören nach `vertilus-docs` und `knowledge-docs` (`repository-split`).
- Eigene Slicer-Profile und G-Code-Dateien als Dokumente (sie liegen als Anhang im Teileordner, nicht im Register).

## repository-split {#repository-split}

Das Projekt 3D-Lab schreibt in zwei Repositories, damit eine Tatsache nur an einer Stelle steht (`std_00_workflow`) und `knowledge-docs` kundenneutral bleibt:

| Inhalt | Repository |
|---|---|
| Druckmodelle, Skripte, STL, G-Code, Handbuch Chat-Blender-Cura | `pfeilus/3d-druck-docs` (dieses Repository) |
| Vision und Backlog der 3D-Komponente für Tenants, Entscheidungen | `pfeilus/vertilus-docs` |
| Werkzeugsteckbriefe, Vergleich der 3D-Programme, Machbarkeitsstudie (kundenneutral) | `pfeilus/knowledge-docs` |

Hat ein Chat in 3D-Lab beide Themen berührt, nennt die Rückmeldung am Ende, in welches Repository welche Änderung gehört. Verweise auf die anderen Repositories laufen über `vertilus:<id>` und `knowledge:<id>`.

## workflow-delta {#workflow-delta}

- **Repository:** `pfeilus/3d-druck-docs` (privat, Branch `main`), zugleich Quelle des claude.ai-Projekts 3D-Lab. Einrichtung und Grenzen: `std_05_github-setup.md`.
- **Stufe 1 (ohne Rückfrage):** Einträge in `changelog`, Zeilen im `registry`, Druckwerte und Ergebnisse in Teiledateien (z. B. `shaver-housing`), vom Nutzer ausdrücklich genannte Korrekturen.
- **Stufe 2 (nach Freigabe):** `project`, `workflow-claude-blender-cura`, neue Teiledateien, alles, was an Dritte geht. Ist die Zuordnung unklar, gilt Stufe 2.
- **Präfixe und Namen:** nur `int_`. Kapitel: Kern 00 bis 09 (`03` changelog, `06` registry, `04` und `05` frei), Arbeitsabläufe 10 bis 19, Teile 20 bis 29 (je Teil eine Datei, ID `<teil>`), Werkzeuge 30 bis 39 bei Bedarf.
- **Anhänge:** Skripte, Modelle und G-Code liegen unter `parts/<teil>/<version>/` (Skript im Versionsordner, Unterordner `stl/` und `gcode/`), Cura-Profile unter `profiles/cura/`. Dateinamen englisch in Kleinbuchstaben (G-Code behält den Namen aus Cura), keine `int_`-Namen, nicht im Register. Jedes Skript nennt im Kopf Blender-Version und Teil-ID.
- **Sonderregeln:** Ein Skript wird vor der Übergabe headless in der Blender-Version des Nutzers getestet (Volumen, offene Kanten, Maße). Maße unbekannter Bauteile werden nie geraten, sondern als `[OFFEN]` geführt.

---

### changelog
- 2026-11-08 – claude.ai-Projekt heißt 3D-Lab, Abschnitt `repository-split` ergänzt (ein Projekt, zwei Repositories). Anlass: Entscheidung des Betreibers im Chat.
- 2026-11-08 – Projektdatei angelegt (Entwurf). Anlass: Der Ablauf Claude, Blender, Cura hat beim Rasierer-Gehäuse funktioniert und soll wiederholbar festgehalten werden.
