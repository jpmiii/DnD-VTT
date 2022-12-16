
bl_info = {
    "name": "D&D VTT RPG Interface",
    "description": "Online 3D RPG Tabletop",
    "author": "Jim McCall",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "category": "Interface",
}
import random
import bpy
import http.client, urllib.parse
import re
from bpy.props import *
import os
import _pickle as pickle
import mathutils
import math
import ssl
from base64 import b64encode
import subprocess as sp


def initSceneProperties():

    bpy.types.Scene.LastUpdate = StringProperty(
        name="LastUpdate",
        default="1", )
    bpy.types.Scene.IP_ADDR = StringProperty(
        name="IP_ADDR",
        default="")
    bpy.types.Scene.PORT = StringProperty(
        name="PORT",
        default="22334")
    bpy.types.Scene.USER = StringProperty(
        name="USER",
        default="GM")
    bpy.types.Scene.PASS = StringProperty(
        name="PASS",
        default="qqq")
    bpy.types.Scene.BLENDFILES = StringProperty(
        name="BLENDFILES",
        default="Z:/")
    bpy.types.Scene.HOST = StringProperty(
        name="HOST",
        default="")
    bpy.types.Scene.BROWSER = StringProperty(
        name="BROWSER",
        default="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    bpy.types.Scene.FeedBack = StringProperty(
        name="I", )
    bpy.types.Scene.AttackMod1 = IntProperty(
        name="Mod1", )
    bpy.types.Scene.Aspect = EnumProperty(
        items=[('H', 'H', 'Highest'),
               ('B', 'B', 'Blunt'),
               ('E', 'E', 'Edge'),
               ('P', 'P', 'Point')],
        name="aspect")
    bpy.types.Scene.AttackType = EnumProperty(
        items=[('Melee', 'Melee', 'Melee'),
               ('Missile', 'Missile', 'Missile')],
        name="Type")
    bpy.types.Scene.Aimzone = EnumProperty(
        items=[('Mid', 'Mid', 'Mid'),
               ('High', 'High', 'High'),
               ('Low', 'Low', 'Low')],
        name="Aim")
    bpy.types.Scene.Action = EnumProperty(
        items=[('target', 'target', 'target'),
               ('attack', 'attack', 'attack'),
               ('dodge', 'dodge', 'dodge'),
               ('block', 'block', 'block'),
               ('counterstrike', 'counterstrike', 'counterstrike'),
               ('ignore', 'ignore', 'ignore')],
        name="Action")

    # scn['loc1'] = 6

    bpy.types.Scene.loc1 = EnumProperty(
        items=[('head', 'skull', '1d6'),
               ('torso', 'torso', '2d6'),
               ('arm', 'arm', '3d6'),
               ('leg', 'leg', '4d6'),
               ('arm', 'face', '3d6'),
               ('leg', 'neck', '4d6'),

               ('arm', 'chest', '3d6'),
               ('leg', 'abdomen', '4d6'),
               ('arm', 'upperarm', '3d6'),
               ('leg', 'elbow', '4d6'),

               ('arm', 'lowerarm', '3d6'),
               ('leg', 'hand', '4d6'),
               ('arm', 'back', '3d6'),
               ('leg', 'butt', '4d6'),

               ('arm', 'groin', '3d6'),
               ('leg', 'thigh', '4d6'),
               ('arm', 'knee', '3d6'),
               ('leg', 'shin', '4d6'),

               ('arm', 'calf', '3d6'),
               ('leg', 'foot', '4d6'),
               ('arm', 'trunk', '3d6'),
               ('leg', 'limb', '4d6'),
               ('arm', 'tentacle', '3d6'),
               ('leg', 'thorax', '4d6'),
               ('arm', 'stalk', '3d6'),
               ('leg', 'body', '4d6'), ],
        name="DamageLoc")

    bpy.types.Scene.weapons = EnumProperty(
        items=[
            ('Shield(Round)', 'Shield(Round)', 'Shield(Round)'),
            ('Shield(Kite)', 'Shield(Kite)', 'Shield(Kite)'),
            ('Shield(Knight)', 'Shield(Knight)', 'Shield(Knight)'),
            ('Shield(Tower)', 'Shield(Tower)', 'Shield(Tower)'),
            ('Shield(Buckler)', 'Shield(Buckler)', 'Shield(Buckler)'),
            ('Dagger', 'Dagger', 'Dagger'),
            ('Keltan', 'Keltan', 'Keltan'),
            ('Knife', 'Knife', 'Knife'),
            ('Taburi', 'Taburi', 'Taburi'),
            ('Sword(Longknife)', 'Sword(Longknife)', 'Sword(Longknife)'),
            ('Sword(Shortsword)', 'Sword(Shortsword)', 'Sword(Shortsword)'),
            ('Mankar', 'Mankar', 'Mankar'),
            ('Mang', 'Mang', 'Mang'),
            ('Sword(Broadsword)', 'Sword(Broadsword)', 'Sword(Broadsword)'),
            ('Sword(StarSteel)', 'Sword(StarSteel)', 'Sword(StarSteel)'),
            ('Sword(Estoc)', 'Sword(Estoc)', 'Sword(Estoc)'),
            ('Sword(Falchion)', 'Sword(Falchion)', 'Sword(Falchion)'),
            ('Sword(Bastard Sword)', 'Sword(Bastard Sword)', 'Sword(Bastard Sword)'),
            ('Sword(Battlesword)', 'Sword(Battlesword)', 'Sword(Battlesword)'),
            ('Club', 'Club', 'Club'),
            ('Club(Mace)', 'Club(Mace)', 'Club(Mace)'),
            ('Club(Morningstar)', 'Club(Morningstar)', 'Club(Morningstar)'),
            ('Club(Maul)', 'Club(Maul)', 'Club(Maul)'),
            ('Hatchet', 'Hatchet', 'Hatchet'),
            ('Axe(Handaxe)', 'Axe(Handaxe)', 'Axe(Handaxe)'),
            ('Axe(Warhammer)', 'Axe(Warhammer)', 'Axe(Warhammer)'),
            ('Axe(Battleaxe)', 'Axe(Battleaxe)', 'Axe(Battleaxe)'),
            ('Flail(Grainflail)', 'Flail(Grainflail)', 'Flail(Grainflail)'),
            ('Flail(Ball & Chain)', 'Flail(Ball & Chain)', 'Flail(Ball & Chain)'),
            ('Flail(Warflail)', 'Flail(Warflail)', 'Flail(Warflail)'),
            ('Spear(Staff)', 'Spear(Staff)', 'Spear(Staff)'),
            ('Spear(Javelin)', 'Spear(Javelin)', 'Spear(Javelin)'),
            ('Spear(Spear)', 'Spear(Spear)', 'Spear(Spear)'),
            ('Spear(Trident)', 'Spear(Trident)', 'Spear(Trident)'),
            ('Polearm(Lance)', 'Polearm(Lance)', 'Polearm(Lance)'),
            ('Polearm(Poleaxe)', 'Polearm(Poleaxe)', 'Polearm(Poleaxe)'),
            ('Polearm(Pike)', 'Polearm(Pike)', 'Polearm(Pike)'),
            ('Lightsabre', 'Lightsabre', 'Lightsabre'),
            ('Bow(Crossbow)', 'Bow(Crossbow)', 'Bow(Crossbow)'),
            ('Bow(Longbow)', 'Bow(Longbow)', 'Bow(Longbow)'),
            ('Compound Bow', 'Compound Bow', 'Compound Bow'),
            ('Bow(Shortbow)', 'Bow(Shortbow)', 'Bow(Shortbow)'),
            ('Bow(Hartbow)', 'Bow(Hartbow)', 'Bow(Hartbow)'),
            ('Unarmed(Kick)', 'Unarmed(Kick)', 'Unarmed(Kick)'),
            ('Unarmed(Punch)', 'Unarmed(Punch)', 'Unarmed(Punch)'),
            ('Unarmed(Grapple)', 'Unarmed(Grapple)', 'Unarmed(Grapple)'),
            ('Unarmed(Claw)', 'Unarmed(Claw)', 'Unarmed(Claw)'),
            ('Unarmed(Bite)', 'Unarmed(Bite)', 'Unarmed(Bite)'),
            ('Unarmed(Tramble)', 'Unarmed(Tramble)', 'Unarmed(Tramble)'),
            ('Bow(Minicrossbow)', 'Bow(Minicrossbow)', 'Bow(Minicrossbow)'),
        ],
        name="Weapons")

    return


initSceneProperties()


class UPDATE_PT_text(bpy.types.Panel):
    """Creates a Panelfor obj in bpy.datavisabili"""
    bl_label = "Update Panel"
    bl_idname = "UPDATE_PT_text"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        scn = context.scene
        row = layout.row()
        # row.label(text="LU: {}".format(bpy.context.scene['LastUpdate']))
        row.prop(scn, 'LastUpdate')
        row = layout.row()
        row.operator("wm.save")

        # row = layout.row()
        row.operator("wm.draw")
        row = layout.row()
        row.operator("wm.update")
        row = layout.row()
        row.prop(scn, 'FeedBack')


class LOGIN_PT_3d(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Login Panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RPG"

    # bl_context = "object"

    def draw(self, context):
        layout = self.layout

        scn = context.scene
        row = layout.row()
        # row.label(text="LU: {}".format(bpy.context.scene['LastUpdate']))
        row.prop(scn, 'IP_ADDR')
        row = layout.row()
        row.prop(scn, 'PORT')
        row = layout.row()
        row.prop(scn, 'USER')
        row = layout.row()
        row.prop(scn, 'PASS')
        row = layout.row()
        row.prop(scn, 'BLENDFILES')
        row = layout.row()
        row.prop(scn, 'HOST')
        row = layout.row()
        row.prop(scn, 'BROWSER')
        row = layout.row()


class UPDATE_PT_3d(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Update Panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RPG"

    # bl_context = "object"

    def draw(self, context):
        layout = self.layout

        scn = context.scene
        row = layout.row()
        # row.label(text="LU: {}".format(bpy.context.scene['LastUpdate']))
        row.prop(scn, 'LastUpdate')
        row = layout.row()
        row.operator("wm.save")
        row.operator("wm.draw")
        row = layout.row()
        row.operator("wm.update")
        row = layout.row()
        row.prop(scn, 'FeedBack')


class ATK_PT_3d(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Roll Panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RPG"

    # bl_context = "object"

    def draw(self, context):
        layout = self.layout

        scn = context.scene
        row = layout.row()

        row.operator("wm.snap")


class CHAR_PT_text(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Character Panel"
    bl_idname = "CHAR_PT_text"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_context = "object"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        row = layout.row()
        row.operator("wm.roll")
        row = layout.row()
        row.operator("wm.getsheet")
        row = layout.row()
        row.operator("wm.gamify")
        row = layout.row()
        row.prop(scn, 'Action')
        row = layout.row()
        row.prop(scn, 'AttackMod1')
        row = layout.row()
        row.prop(scn, 'Aspect')
        row = layout.row()
        row.prop(scn, 'AttackType')
        row = layout.row()
        row.prop(scn, 'Aimzone')
        row = layout.row()
        row.prop(scn, 'weapons')
        row = layout.row()
        #row.operator("wm.attack")

        """row.prop(scn, 'loc1')
        obj = context.object
        if 'Value1' in obj.keys():
            

            row = layout.row()
            row.label(text="value1 is: " + str(obj["Value1"]))
            row = layout.row()
            row.prop(obj, '["Value1"]')"""


###################################

def arm_in(obj):
    outstr = ""
    for x in obj.pose.bones:
        if len(outstr) > 1: outstr = "{}:".format(outstr)
        outstr = "{}{};{},{},{},{},{},{},{}".format(outstr, x.name, x.rotation_quaternion[0], x.rotation_quaternion[1],
                                                    x.rotation_quaternion[2], x.rotation_quaternion[3], x.location[0],
                                                    x.location[1], x.location[2])
    return outstr


def arm_out(obj, in_str):
    pbones = re.split(':', in_str)
    for x in pbones:
        pbone = re.split(';', x)
        if len(pbone) > 1:
            rot = re.split(',', pbone[1])
            if pbone[0] in obj.pose.bones:
                obj.pose.bones[pbone[0]].rotation_quaternion = [float(rot[0]), float(rot[1]), float(rot[2]),
                                                                float(rot[3])]
                obj.pose.bones[pbone[0]].location = [float(rot[4]), float(rot[5]), float(rot[6])]


def matrix44_out(jobj, in_str):
    matrix = re.split(',', in_str)

    jobj.matrix_world[0][0] = float(matrix[0])
    jobj.matrix_world[0][1] = float(matrix[1])
    jobj.matrix_world[0][2] = float(matrix[2])
    jobj.matrix_world[0][3] = float(matrix[3])
    jobj.matrix_world[1][0] = float(matrix[4])
    jobj.matrix_world[1][1] = float(matrix[5])
    jobj.matrix_world[1][2] = float(matrix[6])
    jobj.matrix_world[1][3] = float(matrix[7])
    jobj.matrix_world[2][0] = float(matrix[8])
    jobj.matrix_world[2][1] = float(matrix[9])
    jobj.matrix_world[2][2] = float(matrix[10])
    jobj.matrix_world[2][3] = float(matrix[11])
    jobj.matrix_world[3][0] = float(matrix[12])
    jobj.matrix_world[3][1] = float(matrix[13])
    jobj.matrix_world[3][2] = float(matrix[14])
    jobj.matrix_world[3][3] = float(matrix[15])


def matrix44_in(matrix):
    return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(matrix[0][0], \
                                                                    matrix[0][1], \
                                                                    matrix[0][2], \
                                                                    matrix[0][3], \
                                                                    matrix[1][0], \
                                                                    matrix[1][1], \
                                                                    matrix[1][2], \
                                                                    matrix[1][3], \
                                                                    matrix[2][0], \
                                                                    matrix[2][1], \
                                                                    matrix[2][2], \
                                                                    matrix[2][3], \
                                                                    matrix[3][0], \
                                                                    matrix[3][1], \
                                                                    matrix[3][2], \
                                                                    matrix[3][3])


def vect3tolist(vect):
    return [vect[0], vect[1], vect[2]]


def vect4tolist(vect):
    return [vect[0], vect[1], vect[2], vect[3]]


def matrix4x4tolist(matrix):
    return [vect4tolist(matrix[0]), vect4tolist(matrix[1]), vect4tolist(matrix[2]), vect4tolist(matrix[3])]


class SAVE_OP(bpy.types.Operator):
    bl_idname = "wm.save"
    bl_label = "Save"

    def execute(self, context):

        object_dict = {}

        for sobj in bpy.data.objects:

            if "btype" in sobj.keys() and "hide" not in sobj.keys():
                sobj['hide'] = sobj.hide_get()

            if ("btype" in sobj.keys()) and ((sobj in bpy.context.selected_objects) or (sobj['hide'] != sobj.hide_get()) or ("auto" in sobj.keys())):

                object_dict[sobj.name] = {}
                object_dict[sobj.name]['matrix_world'] = matrix4x4tolist(sobj.matrix_world)
                object_dict[sobj.name]['btype'] = sobj.type
                if sobj.parent is not None:
                    object_dict[sobj.name]['parent'] = sobj.parent.name
                else:
                    object_dict[sobj.name]['parent'] = None
                object_dict[sobj.name]['gametype'] = sobj['gametype']
                if "rot" in sobj:
                    object_dict[sobj.name]['rot'] = sobj['rot']
                if "move" in sobj:
                    object_dict[sobj.name]['move'] = sobj['move']
                if "turn" in sobj:
                    object_dict[sobj.name]['turn'] = sobj['turn']
                if "up" in sobj:
                    object_dict[sobj.name]['up'] = sobj['up']
                if "command" in sobj:
                    object_dict[sobj.name]['command'] = sobj['command']
                if "char_key" in sobj:
                    object_dict[sobj.name]['char_key'] = sobj['char_key']
                if "remove" in sobj:
                    object_dict[sobj.name]['remove'] = sobj['remove']
                if "copyof" in sobj:
                    object_dict[sobj.name]['copyof'] = sobj['copyof']
                object_dict[sobj.name]['uriref'] = sobj['uriref']
                if sobj.type == 'ARMATURE':
                    object_dict[sobj.name]['ARMATURE'] = arm_in(sobj)
                if sobj.type == 'LIGHT':
                    object_dict[sobj.name]['energy'] = sobj.data.energy
                object_dict[sobj.name]['hide'] = sobj.hide_get()
                sobj['hide'] = sobj.hide_get()

            elif sobj in bpy.context.selected_objects and sobj.parent is not None:
                if "btype" in sobj.parent.keys() and sobj.parent not in bpy.context.selected_objects:
                    object_dict[sobj.parent.name] = {}
                    object_dict[sobj.parent.name]['matrix_world'] = matrix4x4tolist(sobj.parent.matrix_world)
                    object_dict[sobj.parent.name]['btype'] = sobj.parent.type
                    if sobj.parent.parent != None:
                        object_dict[sobj.parent.name]['parent'] = sobj.parent.parent.name
                    else:
                        object_dict[sobj.parent.name]['parent'] = None
                    object_dict[sobj.parent.name]['gametype'] = sobj.parent['gametype']
                    if "command" in sobj.parent:
                        object_dict[sobj.parent.name]['command'] = sobj.parent['command']
                    if "copyof" in sobj.parent:
                        object_dict[sobj.parent.name]['copyof'] = sobj.parent['copyof']
                    object_dict[sobj.parent.name]['uriref'] = sobj.parent['uriref']
                    if sobj.parent.type == 'ARMATURE':
                        object_dict[sobj.parent.name]['ARMATURE'] = arm_in(sobj.parent)

        ba = "{}:{}".format(bpy.context.scene.USER, bpy.context.scene.PASS)

        userAndPass = b64encode(ba.encode()).decode("ascii")

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   'Authorization': 'Basic {}'.format(userAndPass)}

        new_ip = bpy.context.scene.IP_ADDR
        folde = ""
        na = new_ip.split("/")
        if len(na) > 1:
            
            new_ip = na[0]
            folde = "/" + na[1]
        conn = http.client.HTTPSConnection(new_ip, bpy.context.scene.PORT,
                                           context=ssl._create_unverified_context())
        #conn.request("POST", "{}/blenderupdate".format(folde), params, headers)
        conn.request("POST", "{}/blendersave".format(folde), pickle.dumps(object_dict, 2), headers)
        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason)
        conn.close()
        gotback = data.decode('ascii')

        print(gotback)
        bpy.context.scene['FeedBack'] = "{} {} {}".format(response.status, response.reason, gotback)

        # bpy.context.scene['LastUpdate'] = gotback

        return {'FINISHED'}

    def invoke(self, context, event):

        return self.execute(context)


class DrawOp(bpy.types.Operator):
    bl_idname = "wm.draw"
    bl_label = "Draw"

    def execute(self, context):

        object_dict = {}

        out = ""
        oname = bpy.data.grease_pencils["Annotations"].layers.active.info

        for i, stroke in bpy.data.grease_pencils["Annotations"].layers[oname].active_frame.strokes.items():
            # print(stroke)
            for p in stroke.points:
                out = out + "{},{},{};".format(p.co[0], p.co[1], p.co[2])
            out = out[:-1] + "\n"

        object_dict[oname] = {}
        object_dict[oname]['strokes'] = out[:-1]
        c = bpy.data.grease_pencils["Annotations"].layers[oname].color
        object_dict[oname]['color'] = "{},{},{}".format(c[0], c[1], c[2])
        object_dict[oname]['thickness'] = bpy.data.grease_pencils["Annotations"].layers[oname].thickness
        object_dict[oname]['btype'] = "Gpencil"
        object_dict[oname]['gametype'] = "Gpencil"

        ba = "{}:{}".format(bpy.context.scene.USER, bpy.context.scene.PASS)

        userAndPass = b64encode(ba.encode()).decode("ascii")

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   'Authorization': 'Basic {}'.format(userAndPass)}


        new_ip = bpy.context.scene.IP_ADDR
        folde = ""
        na = new_ip.split("/")
        if len(na) > 1:
            
            new_ip = na[0]
            folde = "/" + na[1]
        conn = http.client.HTTPSConnection(new_ip, bpy.context.scene.PORT,
                                           context=ssl._create_unverified_context())
        #conn.request("POST", "{}/blenderupdate".format(folde), params, headers)
        conn.request("POST", "{}/blendersave".format(folde), pickle.dumps(object_dict, 2), headers)

        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason)
        conn.close()
        gotback = data.decode('ascii')

        print(gotback)
        bpy.context.scene['FeedBack'] = "{} {} {}".format(response.status, response.reason, gotback)

        return {'FINISHED'}

    def invoke(self, context, event):

        return self.execute(context)


class UPDATE_OP(bpy.types.Operator):
    bl_idname = "wm.update"
    bl_label = "Update"

    def execute(self, context):

        params = urllib.parse.urlencode({'last_update': bpy.context.scene.LastUpdate})

        ba = "{}:{}".format(bpy.context.scene.USER, bpy.context.scene.PASS)

        userAndPass = b64encode(ba.encode()).decode("ascii")

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   'Authorization': 'Basic {}'.format(userAndPass)}
        new_ip = bpy.context.scene.IP_ADDR
        folde = ""
        na = new_ip.split("/")
        if len(na) > 1:
            
            new_ip = na[0]
            folde = "/" + na[1]
        conn = http.client.HTTPSConnection(new_ip, bpy.context.scene.PORT,
                                           context=ssl._create_unverified_context())
        conn.request("POST", "{}/blenderupdate".format(folde), params, headers)
        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason)
        conn.close()
        gotback = pickle.loads(data)

        # print (gotback)
        bpy.context.scene['LastUpdate'] = str(gotback['lu'])
        for obj in gotback:
            if obj.startswith("GG"):
                if "command" in gotback[obj]:
                    print(gotback[obj]["command"])
                    commandlist = re.split("\r\n", gotback[obj]["command"])
                    for comm in commandlist:
                        p1 = comm.split()
                        if p1[0] == "append":
                            bpy.ops.wm.append(filename=p1[1], directory="{}{}".format(bpy.context.scene.BLENDFILES, p1[2]), active_collection=False)

                            print("appended")
                        if p1[0] == "hide":
                            vlayer = bpy.context.scene.view_layers['View Layer']
                            if len(p1) == 2:
                                vlayer.layer_collection.children[p1[1]].exclude = True
                            if len(p1) == 3:
                                vlayer.layer_collection.children[p1[1]].children[p1[2]].exclude = True
                        if p1[0] == "show":
                            vlayer = bpy.context.scene.view_layers['View Layer']
                            if len(p1) == 2:
                                vlayer.layer_collection.children[p1[1]].exclude = False
                            if len(p1) == 3:
                                vlayer.layer_collection.children[p1[1]].children[p1[2]].exclude = False
                        if p1[0] == "ohide" and p1[1] in bpy.data.objects:
                            bpy.data.objects[p1[1]].hide_set(True)
                        if p1[0] == "oshow" and p1[1] in bpy.data.objects:
                            bpy.data.objects[p1[1]].hide_set(False)
                    print("command")
            elif obj == "lu":
                pass
            elif 'strokes' in gotback[obj] and "Annotations" in bpy.data.grease_pencils:
                # print(gotback[obj]['strokes'])
                strks = gotback[obj]['strokes'].split("\n")
                if obj in bpy.data.grease_pencils["Annotations"].layers:
                    N = bpy.data.grease_pencils["Annotations"].layers[obj]
                    if len(N.frames) > 0:
                        AF = N.active_frame
                        AF.clear()
                    else:
                        AF = N.frames.new(0)
                else:
                    N = bpy.data.grease_pencils["Annotations"].layers.new(obj)
                    AF = N.frames.new(0)
                c = gotback[obj]['color'].split(",")
                N.color = (float(c[0]), float(c[1]), float(c[2]))
                N.thickness = int(gotback[obj]['thickness'])
                for strk in strks:
                    new_strk = AF.strokes.new()
                    new_strk.display_mode = "3DSPACE"
                    pnts = strk.split(";")
                    new_strk.points.add(len(pnts))
                    i = 0
                    for pt in pnts:
                        p = pt.split(",")
                        # print(i, p)
                        new_strk.points[i].co = (float(p[0]), float(p[1]), float(p[2]))
                        i = i + 1
            elif obj in bpy.data.objects:
                bobj = bpy.data.objects[obj]
                if 'remove' in gotback[obj]:
                    bpy.data.objects.remove(bobj, do_unlink=True)
                else:
                    bobj['btype'] = bobj.type
                    bobj['gametype'] = gotback[obj]['gametype']
                    bobj['uriref'] = gotback[obj]['uriref']
                    if "copyof" in gotback[obj]:
                        bobj['copyof'] = gotback[obj]['copyof']
                    if "char_key" in gotback[obj]:
                        bobj['char_key'] = gotback[obj]['char_key']
                    bobj.matrix_world = mathutils.Matrix(gotback[obj]['matrix_world'])
                    if 'energy' in gotback[obj]:
                        bobj.data.energy = float(gotback[obj]['energy'])
                    if "ARMATURE" in gotback[obj]:
                        arm_out(bobj, gotback[obj]['ARMATURE'])
                    if "hide" in gotback[obj]:
                        bobj.hide_set(gotback[obj]['hide'])
                        bobj["hide"] = gotback[obj]['hide']
                    if "rot" in gotback[obj]:
                        if gotback[obj]['rot'] != 0:
                            bobj.rotation_euler[2] = bobj.rotation_euler[2] + math.radians(float(gotback[obj]['rot']))
                            bobj["rot"] = 0
                    if "move" in gotback[obj]:
                        if gotback[obj]["move"] != 0:
                            vec = mathutils.Vector((0.0, float(gotback[obj]["move"]), 0.0))
                            inv = bobj.rotation_euler.to_matrix()
                            inv.invert()

                            vec_rot = vec @ inv
                            bobj.location = bobj.location + vec_rot
                            bobj["move"] = 0
                    if "up" in gotback[obj]:
                        if gotback[obj]["up"] != 0:
                            vec = mathutils.Vector((0.0, 0.0, float(gotback[obj]["up"])))
                            inv = bobj.rotation_euler.to_matrix()
                            inv.invert()

                            vec_rot = vec @ inv
                            bobj.location = bobj.location + vec_rot
                            bobj["up"] = 0
                    if "turn" in gotback[obj]:
                        if gotback[obj]['turn'] != 0:
                            bobj.rotation_euler[2] = bobj.rotation_euler[2] + math.radians(float(gotback[obj]['turn']))
                            bobj["turn"] = 0
            elif "copyof" in gotback[obj]:
                p1 = gotback[obj]["copyof"].split(" ")
                # print(obj)
                template_ob = bpy.data.objects.get(p1[0])
                # print(template_ob.name)
                if template_ob:
                    vlayer = bpy.context.scene.view_layers['View Layer']

                    ob = template_ob.copy()
                    ob.name = obj
                    ob['btype'] = ob.type
                    ob['gametype'] = gotback[obj]['gametype']
                    ob['uriref'] = gotback[obj]['uriref']
                    ob['copyof'] = gotback[obj]['copyof']
                    if "char_key" in gotback[obj]:
                        ob['char_key'] = gotback[obj]['char_key']
                    ob.matrix_world = mathutils.Matrix(gotback[obj]['matrix_world'])
                    if len(p1) == 1:
                        vlayer.layer_collection.collection.children['NPCs'].objects.link(ob)
                    if len(p1) == 2:
                        print(p1[1])
                        vlayer.layer_collection.collection.children[p1[1]].objects.link(ob)
                    if len(p1) == 3:
                        view_layer.active_layer_collection.collection.children[p1[1]].children[p1[2]].objects.link(ob)
                    for obc in template_ob.children:
                        obx = obc.copy()

                        if ob.type == 'ARMATURE':
                            obx.parent = ob
                            obx.parent_type = 'ARMATURE'
                        else:
                            obx.parent = ob

                        obx.matrix_world = mathutils.Matrix(gotback[obj]['matrix_world'])
                        if len(p1) == 1:
                            vlayer.layer_collection.collection.children['NPCs'].objects.link(obx)
                        if len(p1) == 2:
                            print(p1[1])
                            vlayer.layer_collection.collection.children[p1[1]].objects.link(obx)
                        if len(p1) == 3:
                            view_layer.active_layer_collection.collection.children[p1[1]].children[p1[2]].objects.link(
                                obx)
                        if obc.parent_type == 'BONE':
                            obx.parent = ob
                            obx.parent_type = 'BONE'

        bpy.context.scene['FeedBack'] = "{} {}".format(response.status, response.reason)
        return {'FINISHED'}

    def invoke(self, context, event):

        return self.execute(context)


class GAMIFY_OP(bpy.types.Operator):
    bl_idname = "wm.gamify"
    bl_label = "Gamify"

    def execute(self, context):
        for sobj in bpy.context.selected_objects:
            print(sobj)
            sobj["btype"] = sobj.type
            sobj["gametype"] = "Item"
            sobj["uriref"] = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(8))
            sobj["copyof"] = sobj.name
            #sobj["char_key"] = sobj.name
            sobj["hide"] = sobj.hide_get()
        bpy.context.scene['FeedBack'] = "gamified"

        # print(sobj.game.properties.keys())
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class SNAP_OP(bpy.types.Operator):
    bl_idname = "wm.snap"
    bl_label = "Snap to Cursor"

    def execute(self, context):
        
        return {'FINISHED'}

    def invoke(self, context, event):
        bpy.ops.view3d.snap_selected_to_cursor()
        return self.execute(context)


class ROLL_OP(bpy.types.Operator):
    bl_idname = "wm.roll"
    bl_label = "Roll Init"

    def execute(self, context):

        for r in bpy.context.selected_objects:
            if "btype" in r.keys():
                sheet_key = "-"
                if "char_key" in r.keys():
                    sheet_key = r['char_key']
                if len(bpy.context.selected_objects) > 1:
                    print(sheet_key)
                    params = urllib.parse.urlencode(
                        {'key': r.name, 'roll_name': 'Initiative', 'roll_type': 'init', 'out_type':'text',
                         'roll_string': '1d20', 'Init Bonus_key': '- initiative_bonus', 'quiet': True})
                else:
                    params = urllib.parse.urlencode(
                        {'key': r.name, 'roll_name': 'Initiative', 'roll_type': 'init', 'out_type':'text',
                         'roll_string': '1d20', 'Init Bonus_key': '- initiative_bonus'})

                ba = "{}:{}".format(bpy.context.scene.USER, bpy.context.scene.PASS)

                userAndPass = b64encode(ba.encode()).decode("ascii")

                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                           'Authorization': 'Basic {}'.format(userAndPass)}

                new_ip = bpy.context.scene.IP_ADDR
                folde = ""
                na = new_ip.split("/")
                if len(na) > 1:
                    
                    new_ip = na[0]
                    folde = "/" + na[1]
                conn = http.client.HTTPSConnection(new_ip, bpy.context.scene.PORT,
                                                context=ssl._create_unverified_context())
                conn.request("POST", "{}/roller".format(folde), params, headers)

                response = conn.getresponse()
                data = response.read()
                print(response.status, response.reason)
                conn.close()
                gotback = data.decode('ascii')
                if 'log' in bpy.data.texts:
                    bpy.data.texts['log'].write('\n{}\n'.format(gotback))
                else:
                    l = bpy.data.texts.new('log')
                    l.write('\n{}\n'.format(gotback))
                bpy.context.scene['FeedBack'] = "{} {}".format(response.status, response.reason)

        # print("done")
        return {'FINISHED'}

    def invoke(self, context, event):

        return self.execute(context)


class getTextSheet(bpy.types.Operator):
    bl_idname = "wm.getsheet"
    bl_label = "Get Sheet"

    def execute(self, context):

        if "char_key" in bpy.context.selected_objects[0].keys():

            params = urllib.parse.urlencode({'key': bpy.context.selected_objects[0]["char_key"]})
        else:
            params = urllib.parse.urlencode({'key': bpy.context.selected_objects[0].name})



        ba = "{}:{}".format(bpy.context.scene.USER, bpy.context.scene.PASS)

        userAndPass = b64encode(ba.encode()).decode("ascii")

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                   'Authorization': 'Basic {}'.format(userAndPass)}


        new_ip = bpy.context.scene.IP_ADDR
        folde = ""
        na = new_ip.split("/")
        if len(na) > 1:
            
            new_ip = na[0]
            folde = "/" + na[1]
        conn = http.client.HTTPSConnection(new_ip, bpy.context.scene.PORT,
                                           context=ssl._create_unverified_context())
        conn.request("POST", "{}/textsheet".format(folde), params, headers)

        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason)
        conn.close()
        gotback = data.decode(encoding='UTF-8', errors='strict')
        if 'TextSheet' in bpy.data.texts:
            bpy.data.texts['TextSheet'].clear()
            bpy.data.texts['TextSheet'].write('\n{}\n'.format(gotback))
        else:
            bpy.data.texts.new("TextSheet")
            bpy.data.texts['TextSheet'].clear()
            bpy.data.texts['TextSheet'].write('\n{}\n'.format(gotback))
        bpy.context.scene['FeedBack'] = "{} {}".format(response.status, response.reason)
        return {'FINISHED'}

    def invoke(self, context, event):

        return self.execute(context)


class getPage(bpy.types.Operator):
    bl_idname = "wm.getpage"
    bl_label = "Get Page"

    def execute(self, context):
        for sobj in bpy.context.selected_objects:
            pid = sp.Popen(
                [bpy.context.scene.BROWSER, "https://{}/sheet?{}".format(bpy.context.scene.HOST, sobj.name)]).pid
            print(sobj.name)
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class removeSelected(bpy.types.Operator):
    bl_idname = "wm.removeselected"
    bl_label = "Remove"

    def execute(self, context):
        for sobj in bpy.context.selected_objects:
            sobj["remove"] = 1
        bpy.context.scene['FeedBack'] = "removed"
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


classes = (
    LOGIN_PT_3d,
    UPDATE_PT_3d,
    ATK_PT_3d,
    UPDATE_PT_text,
    CHAR_PT_text,
    UPDATE_OP,
    GAMIFY_OP,
    ROLL_OP,
    SNAP_OP,
    SAVE_OP,
    DrawOp,
    getTextSheet,
    getPage,
    removeSelected,
)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
