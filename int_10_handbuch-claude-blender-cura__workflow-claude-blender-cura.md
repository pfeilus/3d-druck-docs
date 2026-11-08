# Handbuch: Vom Chat zum Druck (Claude, Blender, Cura)

**ID:** workflow-claude-blender-cura

**Stand:** 08.11.2026 – Entwurf zur Freigabe. Klasse Runbook nach `std_20_dokumentation` (Kurzanleitung zuerst, Hintergrund danach). Getestet mit Blender 5.2.3, Ultimaker Cura 5.12.0 und Anycubic i3 Mega. Stufe 2. Beispielteil: `shaver-housing`.

**Hinweis zu Abschnitts-IDs:** kebab-case, Englisch, Inhalt Deutsch.

---

## quick-guide {#quick-guide}

1. **Auftrag in claude.ai** mit der Vorlage aus `request-template` schreiben und absenden.
2. **Skript speichern:** Claude liefert eine `.py`-Datei. Datei herunterladen und in Blender öffnen oder ihren Inhalt kopieren.
3. **Blender, Arbeitsbereich „Scripting“** (Reiter oben): im Text Editor links „New“ klicken, Skript einfügen (Strg+V), Play-Schaltfläche drücken (oder Alt+P).
4. **Modell ansehen:** Reiter „Layout“ wählen. Mittlere Maustaste = drehen, Shift + mittlere Maustaste = verschieben, Mausrad = zoomen, Taste Home = alles zeigen.
5. **Parameter ändern:** Reiter „Scripting“, Zahlen am Skriptanfang ändern, Play drücken. Das Skript räumt seine alten Teile selbst weg.
6. **STL exportieren:** beide Teile im Outliner auswählen (Strg + Klick), Datei › Exportieren › STL (.stl), Haken „Selection Only“ setzen, Scale 1,0 lassen, Dateiname ohne Umlaute und Leerzeichen, speichern.
7. **Cura:** Drucker „Anycubic i3 Mega“, STL per Drag & Drop laden, Profil „Normal“ (0,2 mm), Einstellungen nach `cura-settings` prüfen, auf „Slice“ klicken, als `.gcode` speichern.
8. **Drucker:** `.gcode` auf die SD-Karte (FAT32), Dateiname kurz ohne Umlaute, am Drucker über das Menü starten.

Der Drucker liest **keinen STL**. Er braucht G-Code, den nur der Slicer erzeugt.

## request-template {#request-template}

Je genauer die Angaben im Auftrag, desto weniger Rückfragen. Bewährt hat sich:

- Was ist das Teil und wofür (Funktion, eingebaute Bauteile mit Maßen)?
- Zeichnung oder Skizze als Bild, Maße in mm, dazu gewünschte Abweichungen („darf optimiert werden“).
- Drucker, Filament, Düse (hier Anycubic i3 Mega, PLA Basic 1,75 mm, 0,4 mm).
- Gewünschte Dateien: nur Skript für Blender, oder auch STL.
- Besonderheiten: Löcher, Mulden, Passungen, sichtbare Fugen, Druckausrichtung.

Beispiel: „Gehäuse für einen Rasierer in zwei Teilen (Haube für Motor, Elektronik, Akku, und Deckel). Außen soll keine Fuge zu sehen sein. Loch Ø 11 mm für den Einschaltknopf in einer Mulde. Drucker Anycubic i3 Mega, PLA schwarz. Bitte zuerst nur ein Blender-Skript.“

## blender-views {#blender-views}

- **Scripting:** links der Text Editor mit dem Code, rechts davon ein kleiner 3D-Viewport und unten die Python-Konsole mit Meldungen (das Skript meldet hier Volumen und offene Kanten).
- **Layout:** großer 3D-Viewport. Rechts oben der Outliner (Liste der Objekte), hier sind `Rasierer_Haube` und `Rasierer_Deckel` zu finden.
- **Darstellung:** Taste Z öffnet das Menü für Solid und Wireframe. Alt+Z schaltet Röntgen ein, so sieht man in die Hohlräume.
- **Ansichten:** Ziffernblock 1 (vorne), 3 (rechts), 7 (oben). Ziffernblock-Punkt zentriert die Auswahl.
- **Einheiten:** Das Skript stellt die Szene auf Millimeter, die Maße im Viewport sind direkt mm.

## export-stl {#export-stl}

- Auswahl: Das Skript wählt beide Teile am Ende selbst aus. Im Outliner prüfen, beide müssen hell markiert sein.
- Im Export-Fenster rechts unter „Include“ den Haken „Selection Only“ setzen, sonst landet die ganze Szene in der Datei.
- Scale bleibt 1,0, weil die Szene schon in Millimetern vorliegt.
- Alternative: Am Ende des Skripts steht eine auskommentierte Zeile `bpy.ops.wm.stl_export(...)`. Raute entfernen, Pfad anpassen, Skript neu ausführen.
- Dateinamen mit Datum erleichtern das Auseinanderhalten der Versionen, z. B. `Rasierer_20261108.stl`.

## cura-settings {#cura-settings}

Werte aus dem G-Code vom 08.11.2026 (Cura 5.12.0, Drucker „Anycubic i3 Mega“). Die Datei enthält nur Abweichungen vom Profil und die Werte im G-Code selbst, nicht das ganze Profil.

| Einstellung | Wert | Quelle |
|---|---|---|
| Profil | „Normal #2“ (Qualität „Normal“, vom Nutzer angepasst) | Dateiende |
| Schichthöhe | 0,2 mm | Kopf |
| Füllung | 20 % | Dateiende (Abweichung vom Profil) |
| Stützstruktur | aus | Dateiende (Abweichung vom Profil) |
| Düsentemperatur | 200 °C | Kopf (M104) |
| Betttemperatur | 60 °C | Kopf (M140) |
| Rückzug | 6 mm bei 40 mm/s | Kopf |
| Wandlinien | 2 (je Teil Außen- und Innenwand) | abgeleitet aus Schicht 60 |
| Geschwindigkeit | Wände etwa 50 mm/s, Haut etwa 20 mm/s | abgeleitet |
| Lüfter | zuerst 50 %, dann 100 % | abgeleitet |
| Haftung | Skirt (Randlinie) | Kopf |
| Druckzeit, Material | 6393 s (1 h 47 min), 6,93 m Filament | Kopf |

Nicht in der Datei: Materialname, vollständige Profilwerte. Für exakte Wiederholbarkeit in Cura das Profil exportieren (Einstellungen › Profile › Exportieren) und im Repository ablegen.

**Empfehlung:** Bei Wänden von 1,2 mm Dicke passen genau 3 Wandlinien zu 0,4 mm. Mit 2 Linien bleibt ein Restspalt, den die Füllung nur schwach ausfüllt. Daher „Wandlinienanzahl“ auf 3 stellen (Cura: Einstellungen › Wand).

## background {#background}

Der Ablauf trennt Entwurf, Modell und Fertigung. Claude schreibt den Entwurf als Code, deshalb sind Maße als Zahlen am Skriptanfang änderbar und das Modell lässt sich sauber wiederholen. Blender setzt den Code in ein Gitternetz um. Der STL ist nur dieses Gitternetz. Der Slicer schneidet es in Schichten und erzeugt den G-Code für den Drucker.

Vor der Übergabe testet Claude das Skript ohne Oberfläche in derselben Blender-Version und meldet Maße, Volumen und die Zahl offener Kanten (Soll: 0). Offene Kanten (nicht-manifold) machen das Teil für den Slicer unzuverlässig.

## error-patterns {#error-patterns}

| Symptom | Ursache | Abhilfe |
|---|---|---|
| Drucker liest die Datei nicht | STL statt G-Code auf der SD-Karte | in Cura slicen, `.gcode` kopieren |
| Drucker zeigt Datei nicht an | Name mit Umlaut oder Leerzeichen, SD-Karte nicht FAT32 | kurzen Namen wählen, Karte neu formatieren |
| Skript meldet einen Fehler | Skript aus altem Stand oder unvollständig kopiert | Skript neu einfügen und von Claude prüfen lassen, Fehlertext aus der Konsole mitschicken |
| Teile doppelt im Viewport | Skript von Hand umbenannte Objekte nicht gelöscht | nur Objekte `Rasierer_*` löschen oder Skript neu laufen lassen |
| Modell viel zu klein oder groß | Einheiten falsch | Scale im Export auf 1,0 und Szene auf mm prüfen |
| Wand wirkt dünn oder lückig | zu wenige Wandlinien | Wandlinien auf 3 (siehe `cura-settings`) |

---

### changelog
- 2026-11-08 – Erstfassung (Entwurf). Anlass: Der Ablauf hat beim Rasierer-Gehäuse funktioniert. Cura-Werte aus dem G-Code vom 08.11.2026.
