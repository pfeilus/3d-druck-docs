# Rasierer-Gehäuse, Birnenform, außen nahtlos (Haube + Deckel) für Blender 4.x/5.x
# Einfügen: Arbeitsbereich "Scripting" -> Text Editor -> New -> Skript einfügen -> Play (Alt+P)
# Alle Maße in mm. Die Szene wird auf Millimeter gestellt.
import bpy, bmesh, math
from mathutils import Vector, Matrix

# ---------------- Form ----------------
R_BULB = 30.0          # größter Radius unten (Deckelbereich)
R_NECK = 18.0          # Radius im schlanken Kopfbereich
H_TOTAL = 50.0         # Gesamthöhe (Deckel + Haube, montiert)
FILLET = 10.0          # Rundung am Boden (R10 wie in der Zeichnung)
BULB_SHAPE = 0.5       # 0.3 = Verjüngung früher/steiler, 0.7 = später/sanfter
H_COLLAR = 5.0         # Hals für den Rasierkopf
R_COLLAR_BASE, R_COLLAR_TOP, R_HOLE_TOP = 11.5, 10.5, 8.0   # Hals: unten, oben, Bohrung (Ø16)
WALL = 1.2             # Wandstärke
FLOOR = 2.0            # Bodenstärke des Deckels

# ---------------- Fuge Deckel / Haube ----------------
Z_SPLIT = 16.0         # Höhe der Trennfuge (muss über FILLET + 6 liegen)
SEAM_GAP = 0.1         # Spalt der Fuge außen (0 = ohne Spalt)
CLEAR = 0.2            # Spiel zwischen Deckelrand und Haube
LIP_H, LIP_T = 4.5, 1.2   # Höhe und Stärke des Innenrands am Deckel

# ---------------- Schalterloch ----------------
Z_BTN, BTN_D, BTN_ANGLE_DEG = 33.0, 11.0, 270.0   # Höhe, Ø, Richtung (270 = -Y)
POCKET_R, POCKET_DEPTH = 9.0, 2.0                 # Mulde
BOSS_R, BOSS_IN = 10.0, 4.5                       # innere Verstärkung um das Loch

PLATE = True           # True: Druckplatte (Haube umgedreht daneben), False: montiert
SEG = 128              # Umfangsauflösung der Drehkörper

# ---------------- Hilfsfunktionen ----------------
def arc(cr, cz, rad, a0, a1, n=48):
    return [(cr + rad*math.cos(a0 + (a1-a0)*i/n), cz + rad*math.sin(a0 + (a1-a0)*i/n)) for i in range(n+1)]

def bezier(p0, p1, p2, p3, n=60):
    """liefert (Punkt, äußere Normale) entlang einer kubischen Bezierkurve in (r,z)"""
    out = []
    for i in range(n+1):
        t = i/n; u = 1-t
        r = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
        z = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
        dr = 3*(u*u*(p1[0]-p0[0]) + 2*u*t*(p2[0]-p1[0]) + t*t*(p3[0]-p2[0]))
        dz = 3*(u*u*(p1[1]-p0[1]) + 2*u*t*(p2[1]-p1[1]) + t*t*(p3[1]-p2[1]))
        L = math.hypot(dr, dz)
        out.append(((r, z), (dz/L, -dr/L)))
    return out

def to_object(bm, name):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob

def revolve(pts, name):
    """(r,z)-Profil als geschlossener Linienzug -> Drehkörper um die Z-Achse"""
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0.0, z)) for r, z in pts]
    es = [bm.edges.new((vs[i], vs[(i+1) % len(vs)])) for i in range(len(vs))]
    bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1), angle=2*math.pi, steps=SEG)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    loose = [e for e in bm.edges if not e.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context='EDGES')
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return to_object(bm, name)

def cylinder(P, n, radius, t0, t1, name, seg=96):
    """Zylinder entlang der Achse n, von P+t0*n bis P+t1*n"""
    bm = bmesh.new()
    r0 = [bm.verts.new((radius*math.cos(2*math.pi*i/seg), radius*math.sin(2*math.pi*i/seg), t0)) for i in range(seg)]
    r1 = [bm.verts.new((radius*math.cos(2*math.pi*i/seg), radius*math.sin(2*math.pi*i/seg), t1)) for i in range(seg)]
    for i in range(seg):
        j = (i + 1) % seg
        bm.faces.new((r0[i], r0[j], r1[j], r1[i]))
    bm.faces.new(r0[::-1]); bm.faces.new(r1)
    bm.transform(Matrix.Translation(P) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4())
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return to_object(bm, name)

def box(z0, z1, name, h=200.0):
    bm = bmesh.new()
    v = [bm.verts.new((x, y, z)) for x in (-h, h) for y in (-h, h) for z in (z0, z1)]
    for a, b, c, d in ((0,1,3,2), (4,6,7,5), (0,4,5,1), (2,3,7,6), (0,2,6,4), (1,5,7,3)):
        bm.faces.new((v[a], v[b], v[c], v[d]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return to_object(bm, name)

def boolean(obj, tool, op):
    mod = obj.modifiers.new("bool", 'BOOLEAN')
    mod.operation, mod.object, mod.solver = op, tool, 'EXACT'
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool, do_unlink=True)

def duplicate(ob, name):
    new = ob.copy(); new.data = ob.data.copy(); new.name = name
    bpy.context.collection.objects.link(new)
    return new

# ---------------- Szene ----------------
for ob in list(bpy.data.objects):
    if ob.name == 'Cube' or ob.name.startswith(('Rasierer_', 'tmp_')):
        bpy.data.objects.remove(ob, do_unlink=True)
us = bpy.context.scene.unit_settings
us.system, us.scale_length, us.length_unit = 'METRIC', 0.001, 'MILLIMETERS'

# ---------------- Profil (r, z) ----------------
Z_TOP = H_TOTAL - H_COLLAR
R_SHOULDER = R_NECK - R_COLLAR_BASE           # Schulterrundung endet am Halsansatz
Z_SH = Z_TOP - R_SHOULDER                     # Beginn der Schulterrundung
span = Z_SH - FILLET
K = BULB_SHAPE
bz = bezier((R_BULB, FILLET), (R_BULB, FILLET + K*span), (R_NECK, Z_SH - K*span), (R_NECK, Z_SH))
bz_pts = [p for p, _ in bz]

# Außenkontur: Boden-Rundung -> Birnenkurve -> Schulter -> Hals
outer_pts = ([(0, 0)] + arc(R_BULB - FILLET, FILLET, FILLET, -math.pi/2, 0)
             + bz_pts[1:] + arc(R_NECK - R_SHOULDER, Z_SH, R_SHOULDER, 0, math.pi/2)[1:]
             + [(R_COLLAR_TOP, H_TOTAL), (0, H_TOTAL)])

# Innenkontur (Wand überall WALL dick, senkrecht zur Fläche gemessen)
rf = FILLET - FLOOR
bz_in = [(p[0] - WALL*n[0], p[1] - WALL*n[1]) for p, n in bz]
bz_in[0] = (R_BULB - WALL, FILLET); bz_in[-1] = (R_NECK - WALL, Z_SH)
cav_pts = ([(0, FLOOR)] + arc(R_BULB - WALL - rf, FILLET, rf, -math.pi/2, 0)
           + bz_in[1:] + arc(R_NECK - R_SHOULDER, Z_SH, R_SHOULDER - WALL, 0, math.pi/2)[1:]
           + [(0, Z_TOP - WALL)])

def r_outer(z):
    """Außenradius der Birnenkurve in der Höhe z (für z >= FILLET)"""
    for (r0, z0), (r1, z1) in zip(bz_pts, bz_pts[1:]):
        if z0 <= z <= z1:
            return r0 + (r1 - r0)*(z - z0)/(z1 - z0)
    raise ValueError("z außerhalb der Birnenkurve")

# ---------------- Hohlkörper ----------------
shell = revolve(outer_pts, "Rasierer_Hohlkoerper")
boolean(shell, revolve(cav_pts, "tmp_cav"), 'DIFFERENCE')
hole_top = cylinder(Vector((0, 0, Z_TOP - WALL - 1)), Vector((0, 0, 1)), R_HOLE_TOP, 0, H_COLLAR + WALL + 2, "tmp_hole")
boolean(shell, hole_top, 'DIFFERENCE')

# Schalterloch am schlanken Teil
assert FILLET < Z_BTN < Z_SH, "Z_BTN muss auf der Birnenkurve liegen"
for (p0, n0), (p1, n1) in zip(bz, bz[1:]):
    if p0[1] <= Z_BTN <= p1[1]:
        s = (Z_BTN - p0[1])/(p1[1] - p0[1])
        pr = p0[0] + (p1[0] - p0[0])*s
        nr, nz = n0[0] + (n1[0] - n0[0])*s, n0[1] + (n1[1] - n0[1])*s
        break
L = math.hypot(nr, nz); nr, nz = nr/L, nz/L
phi = math.radians(BTN_ANGLE_DEG)
P = Vector((pr*math.cos(phi), pr*math.sin(phi), Z_BTN))
n = Vector((math.cos(phi)*nr, math.sin(phi)*nr, nz))

boss = cylinder(P, n, BOSS_R, -BOSS_IN, 2.0, "tmp_boss")
boolean(boss, revolve(outer_pts, "tmp_env"), 'INTERSECT')   # Verstärkung nur innerhalb der Außenhülle
boolean(shell, boss, 'UNION')
boolean(shell, cylinder(P, n, POCKET_R, -POCKET_DEPTH, 15.0, "tmp_pocket"), 'DIFFERENCE')   # Mulde
boolean(shell, cylinder(P, n, BTN_D/2, -BOSS_IN - 3.0, 6.0, "tmp_btn"), 'DIFFERENCE')       # Loch

# ---------------- Teilen in Deckel und Haube ----------------
lid = duplicate(shell, "Rasierer_Deckel")
cap = shell; cap.name = "Rasierer_Haube"

boolean(lid, box(Z_SPLIT, 300, "tmp_cut_lid"), 'DIFFERENCE')
boolean(cap, box(-300, Z_SPLIT + SEAM_GAP, "tmp_cut_cap"), 'DIFFERENCE')

# Innenrand am Deckel: verdickte Wand unter der Fuge + Führungsring in die Haube hinein
d_ov, d1, d2 = WALL - 0.2, WALL + CLEAR, WALL + CLEAR + LIP_T
za = Z_SPLIT - 4.0 - (d2 - d_ov)              # Beginn der 45°-Anschrägung (unterhalb der Fuge)
zb = Z_SPLIT + LIP_H
assert za > FILLET, "Z_SPLIT zu niedrig"
ring_pts = [(r_outer(za) - d_ov, za), (r_outer(za + d2 - d_ov) - d2, za + d2 - d_ov),
            (r_outer(zb) - d2, zb), (r_outer(zb) - d1, zb),
            (r_outer(Z_SPLIT) - d1, Z_SPLIT), (r_outer(Z_SPLIT) - d_ov, Z_SPLIT)]
boolean(lid, revolve(ring_pts, "tmp_ring"), 'UNION')

# ---------------- Aufräumen (Null-Längen-Kanten aus den Booleans) ----------------
for ob in (cap,):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-4)
    bm.to_mesh(ob.data); bm.free()

# ---------------- Anordnung ----------------
if PLATE:
    cap.location = (-38.0, 0.0, -(Z_SPLIT + SEAM_GAP))   # Haube steht mit der offenen Seite auf dem Druckbett
    lid.location = (38.0, 0.0, 0.0)

# ---------------- Kontrolle ----------------
for ob in (cap, lid):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    print(ob.name, "Volumen: %.0f mm3" % bm.calc_volume(), "| nicht-manifold:", sum(1 for e in bm.edges if not e.is_manifold))
    bm.free()
bpy.ops.object.select_all(action='DESELECT')
cap.select_set(True); lid.select_set(True)

# Optional: STL aus Blender schreiben (Pfad anpassen, Zeilen entkommentieren)
# bpy.ops.wm.stl_export(filepath="C:/Temp/rasierer_birne_druckplatte.stl", export_selected_objects=True)
