# Teil: Rasierer-Gehäuse

**ID:** shaver-housing

**Stand:** 08.11.2026 – Entwurf zur Freigabe. Stufe 1 (Werte und Ergebnisse). Ablauf: `workflow-claude-blender-cura`.

**Hinweis zu Abschnitts-IDs:** kebab-case, Englisch, Inhalt Deutsch.

---

## purpose {#purpose}

Gehäuse für einen Rasierer in zwei Teilen: **Haube** (nimmt Motor, Elektronik und Akku auf, Hals für den Rasierkopf, Schalterloch) und **Deckel** (verschließt unten). Beide Teile werden zusammen auf einer Druckplatte gedruckt, aber als zwei Einzelteile. Ausgangspunkt war eine Zeichnung aus Shapr3D (A3, mm, 1:1), die nicht streng einzuhalten war.

## versions {#versions}

| Version | Form | Ordner und Skript | Stand |
|---|---|---|---|
| 1 | zylindrisch, Ø 60 mm, Höhe 35,4 mm, Flansch an der Fuge | `parts/shaver-housing/v1-flange/`, `shaver_housing_flange_blender.py`, STL in `stl/` | 08.11.2026, funktioniert; außen ein Wulst an der Fuge |
| 2 | Birnenform, unten Ø 60 mm, oben Ø 36 mm, Höhe 50 mm, außen nahtlos | `parts/shaver-housing/v2-pear/`, `shaver_housing_pear_blender.py`, G-Code in `gcode/` | 08.11.2026, gesliced; Druckergebnis `[OFFEN]` |

## parameters-v2 {#parameters-v2}

Werte am Skriptanfang von Version 2:

| Parameter | Wert | Bedeutung |
|---|---|---|
| `R_BULB` / `R_NECK` | 30 / 18 mm | größter Radius unten / Radius im Kopfbereich |
| `H_TOTAL` | 50 mm | Gesamthöhe montiert |
| `FILLET` | 10 mm | Bodenrundung |
| `BULB_SHAPE` | 0,5 | Lage der Verjüngung (0,3 früher, 0,7 später) |
| `H_COLLAR`, Hals | 5 mm hoch, Ø 23 unten, Ø 21 oben, Bohrung Ø 16 | Sitz des Rasierkopfs |
| `WALL` / `FLOOR` | 1,2 / 2,0 mm | Wand- und Bodenstärke |
| `Z_SPLIT` | 16 mm | Höhe der Trennfuge |
| `SEAM_GAP` / `CLEAR` | 0,1 / 0,2 mm | Spalt außen / Spiel des Innenrands |
| `LIP_H` / `LIP_T` | 4,5 / 1,2 mm | Höhe und Stärke des Innenrands am Deckel |
| `Z_BTN`, `BTN_D` | 33 mm, Ø 11 mm | Höhe und Durchmesser des Schalterlochs |
| Mulde, Verstärkung | Ø 18 mm, 2 mm tief; innen Ø 20 mm, 4,5 mm | Mulde um das Loch, innere Verstärkung |
| `PLATE` | True | Druckplatte: Haube links (offene Seite unten), Deckel rechts |

Prüfwerte (Test mit Blender 5.2.3 ohne Oberfläche): Haube 6700 mm³, Deckel 9849 mm³, beide ohne offene Kanten. Maße: Haube 58,2 × 58,2 × 33,9 mm, Deckel 60 × 60 × 20,5 mm.

## print-data {#print-data}

Druck auf Anycubic i3 Mega, PLA Basic 1,75 mm schwarz, Düse 0,4 mm. Die Slicer-Werte (G-Code vom 08.11.2026: 0,2 mm, Füllung 20 %, ohne Stützen, 200 °C Düse, 60 °C Bett, Druckzeit 1 h 47 min, 6,93 m Filament) stehen in `workflow-claude-blender-cura`, `cura-settings`. Ausrichtung: Haube mit der offenen Seite nach unten, Deckel mit der flachen Seite nach unten.

## decisions {#decisions}

- **08.11.2026:** Form 2 (birnenförmig, unten deutlich breiter am Deckel, oben schlank am Rasierkopf) als zusätzliche Testform gewünscht.
- **08.11.2026:** Außen nahtlos, die Verbindung liegt innen (Innenrand am Deckel greift in die Haube).
- **08.11.2026:** Schalterloch am schlanken Teil in einer Mulde, mit innerer Verstärkung gegen Ausreißen der dünnen Wand.
- **08.11.2026:** Zuerst nur Skript, STL erst auf Zuruf; STL wurde danach selbst aus Blender exportiert.

## open-points {#open-points}

- Innenmaße von Motor, Elektronik und Akku sind unbekannt `[OFFEN]`. Der Innenraum ist am Hals nur etwa Ø 33 mm weit, ob alles passt, ist ungeprüft.
- Wandlinien: Im G-Code stehen 2, bei 1,2 mm Wand sind 3 sinnvoll (`workflow-claude-blender-cura`, `cura-settings`).
- Passung von Innenrand und Fuge (0,2 mm Spiel, 0,1 mm Spalt) ist erst nach dem Druck beurteilbar `[OFFEN]`.
- Ergebnis des Drucks (Oberfläche, Passung, Schalterloch) eintragen.

---

### changelog
- 2026-11-08 – Erstfassung (Entwurf). Anlass: Zwei Versionen des Gehäuses wurden entworfen, Version 2 gesliced.
