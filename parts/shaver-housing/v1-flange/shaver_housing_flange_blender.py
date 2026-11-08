# Rasierer-Gehäuse (Haube + Deckel) für Blender 4.x/5.x
# Einfügen: Arbeitsbereich "Scripting" -> Text Editor -> New -> Skript einfügen -> Play (Alt+P)
# Alle Maße in mm. Szene wird auf Millimeter gestellt.
import bpy, bmesh, math
from mathutils import Vector, Matrix

# ---------------- Parameter (mm) ----------------
R_FLANGE, R_FL_IN, H_FLANGE = 30.0, 28.9, 5.0     # unterer Rand der Haube
R_DOME, WALL = 29.0, 1.2                          # Kuppelwand
H_TOTAL, H_COLLAR = 35.42, 5.0
Z_TOP = H_TOTAL - H_COLLAR
R_ARC, R_TOP_FLAT = 17.0, 17.5                    # Rundung R17
R_COLLAR_BASE, R_COLLAR_TOP, R_HOLE_TOP = 11.5, 10.5, 8.0
Z_BTN, BTN_D, BTN_ANGLE_DEG = 25.5, 11.0, 270.0   # Schalterloch (270 = Richtung -Y)
POCKET_R, POCKET_DEPTH = 9.0, 2.0                 # Mulde
BOSS_R, BOSS_IN = 10.0, 4.5                       # innere Verstärkung um das Loch
LID_R_OUT, LID_R_IN = 30.0, 27.5
LID_BOWL_H, LID_LIP_H, LID_LIP_OUT = 13.0, 4.5, 28.7   # 0,2 mm Spiel zur Haube
LID_FLOOR, LID_FILLET = 2.0, 10.0
PLATE = True                                      # True: beide Teile nebeneinander (Druckplatte)
SEG = 128                                         # Umfangsauflösung der Drehkörper

# ---------------- Hilfsfunktionen ----------------
def arc(cr, cz, rad, a0, a1, n=48):
    return [(cr + rad*math.cos(a0 + (a1-a0)*i/n), cz + rad*math.sin(a0 + (a1-a0)*i/n)) for i in range(n+1)]

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

def boolean(obj, tool, op):
    mod = obj.modifiers.new("bool", 'BOOLEAN')
    mod.operation, mod.object, mod.solver = op, tool, 'EXACT'
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(tool, do_unlink=True)

# ---------------- Szene ----------------
for ob in list(bpy.data.objects):
    if ob.name == 'Cube' or ob.name.startswith(('Rasierer_', 'tmp_')):
        bpy.data.objects.remove(ob, do_unlink=True)
us = bpy.context.scene.unit_settings
us.system, us.scale_length, us.length_unit = 'METRIC', 0.001, 'MILLIMETERS'

# ---------------- Haube ----------------
cr = R_DOME - R_ARC
cz = Z_TOP - math.sqrt(R_ARC**2 - (R_TOP_FLAT - cr)**2)
a_end = math.atan2(Z_TOP - cz, R_TOP_FLAT - cr)
outer_pts = ([(0, 0), (R_FLANGE, 0), (R_FLANGE, H_FLANGE), (R_DOME, H_FLANGE)]
             + arc(cr, cz, R_ARC, 0, a_end)
             + [(R_COLLAR_BASE, Z_TOP), (R_COLLAR_TOP, H_TOTAL), (0, H_TOTAL)])
ri = R_ARC - WALL
zi_top = Z_TOP - WALL
ri_end = cr + math.sqrt(ri**2 - (zi_top - cz)**2)
a_end_i = math.atan2(zi_top - cz, ri_end - cr)
cav_pts = ([(0, -1), (R_FL_IN, -1), (R_FL_IN, H_FLANGE), (R_DOME - WALL, H_FLANGE)]
           + arc(cr, cz, ri, 0, a_end_i) + [(0, zi_top)])

cap = revolve(outer_pts, "Rasierer_Haube")
boolean(cap, revolve(cav_pts, "tmp_cav"), 'DIFFERENCE')
hole_top = cylinder(Vector((0, 0, zi_top - 1)), Vector((0, 0, 1)), R_HOLE_TOP, 0, H_TOTAL - zi_top + 2, "tmp_hole")
boolean(cap, hole_top, 'DIFFERENCE')

# Schalterloch auf der Rundung
dz = Z_BTN - cz
pr = cr + math.sqrt(R_ARC**2 - dz**2)
alpha = math.atan2(dz, pr - cr)
phi = math.radians(BTN_ANGLE_DEG)
P = Vector((pr*math.cos(phi), pr*math.sin(phi), Z_BTN))
n = Vector((math.cos(phi)*math.cos(alpha), math.sin(phi)*math.cos(alpha), math.sin(alpha)))

boss = cylinder(P, n, BOSS_R, -BOSS_IN, 2.0, "tmp_boss")
boolean(boss, revolve(outer_pts, "tmp_env"), 'INTERSECT')   # Verstärkung nur innerhalb der Außenhülle
boolean(cap, boss, 'UNION')
boolean(cap, cylinder(P, n, POCKET_R, -POCKET_DEPTH, 15.0, "tmp_pocket"), 'DIFFERENCE')           # Mulde
boolean(cap, cylinder(P, n, BTN_D/2, -BOSS_IN - 3.0, 6.0, "tmp_btn"), 'DIFFERENCE')                # Loch 11 mm

# ---------------- Deckel ----------------
f = LID_FILLET
rf = f - LID_FLOOR
lid_pts = ([(0, 0)] + arc(LID_R_OUT - f, f, f, -math.pi/2, 0)
           + [(LID_R_OUT, LID_BOWL_H), (LID_LIP_OUT, LID_BOWL_H),
              (LID_LIP_OUT, LID_BOWL_H + LID_LIP_H), (LID_R_IN, LID_BOWL_H + LID_LIP_H)]
           + arc(LID_R_IN - rf, f, rf, 0, -math.pi/2) + [(0, LID_FLOOR)])
lid = revolve(lid_pts, "Rasierer_Deckel")

if PLATE:
    cap.location.x, lid.location.x = -36.0, 36.0

# ---------------- Kontrolle ----------------
for ob in (cap, lid):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    print(ob.name, "Volumen: %.0f mm3" % bm.calc_volume(), "Flächen:", len(bm.faces))
    bm.free()
bpy.ops.object.select_all(action='DESELECT')
cap.select_set(True); lid.select_set(True)

# Optional: STL direkt aus Blender schreiben (Pfad anpassen, Zeilen entkommentieren)
# bpy.ops.wm.stl_export(filepath="C:/Temp/rasierer_druckplatte.stl", export_selected_objects=True)
