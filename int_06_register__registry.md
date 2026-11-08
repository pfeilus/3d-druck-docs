# Register 3d-druck

**ID:** registry

**Stand:** 08.11.2026 – eingeführt. Stufe 1 (Zeilen ergänzen und ändern). Namens- und Registerregeln: `std_00_workflow`, `naming-convention`.

**Zweck:** Das Register führt alle `int_`-Dateien dieses Repositories mit ID, Kapitel, übergeordneter Datei, Gegenstück und früheren Namen. Die ID ist maßgeblich, der Dateiname folgt ihr. Nicht im Register: `std_*`, `CLAUDE.md`, `README.md` und die Ordner `parts/` und `profiles/` (siehe `assets`).

**Hinweis zu Abschnitts-IDs:** kebab-case, Englisch, Inhalt Deutsch.

---

## files {#files}

| ID | Datei | Kapitel | übergeordnet | Gegenstück | früher |
|---|---|---|---|---|---|
| `project` | `int_00_3d-druck.md` | Kern | – | – | neu |
| `changelog` | `int_03_changelog__changelog.md` | Kern | – | – | neu |
| `registry` | `int_06_register__registry.md` | Kern | – | – | neu |
| `workflow-claude-blender-cura` | `int_10_handbuch-claude-blender-cura__workflow-claude-blender-cura.md` | Arbeitsabläufe | – | `shaver-housing` | neu |
| `shaver-housing` | `int_20_rasierer-gehaeuse__shaver-housing.md` | Teile | – | `workflow-claude-blender-cura` | neu |

## assets {#assets}

Ausgenommen vom Register, jede Datei gehört zu einem Teil. Ordnerschema: `parts/<teil-id>/<version>/`.

| Pfad | Teil und Version | Stand |
|---|---|---|
| `parts/shaver-housing/v1-flange/shaver_housing_flange_blender.py` | `shaver-housing`, Version 1 (zylindrisch mit Flansch) | 08.11.2026, getestet mit Blender 5.2.3 |
| `parts/shaver-housing/v1-flange/stl/` | Version 1: `shaver_cap.stl`, `shaver_lid.stl`, `shaver_plate_cap_and_lid.stl` | 08.11.2026, mit CadQuery erzeugt, geprüft (geschlossene Körper) |
| `parts/shaver-housing/v2-pear/shaver_housing_pear_blender.py` | `shaver-housing`, Version 2 (Birnenform, nahtlos) | 08.11.2026, getestet mit Blender 5.2.3 |
| `parts/shaver-housing/v2-pear/gcode/AI3M_Rasierer_20261108.gcode` | Version 2, Druckplatte, Cura 5.12.0 | 08.11.2026, Druckergebnis `[OFFEN]` |
| `parts/shaver-housing/v2-pear/stl/` | Version 2: STL aus Blender | `[OFFEN]` noch nicht abgelegt |
| `profiles/cura/` | Cura-Profile (Export), mit `README.md` | Ordner angelegt 08.11.2026; Profil folgt mit dem nächsten Modell |

---

### changelog
- 2026-11-08 – Erstfassung. Anlass: Projektaufbau.
