bl_info = {
            "name": "Retopology",
            "author": "Nikhil Sridhar",
            "version": (2, 5, 2),
            "blender": (2,80,0),
            "location": "View3D > Sideshelf > Retopology",
            "description": "Remesh/Retopologize",
            "warning": "",
            "wiki_url": "",
            "category": "AFXLAB"}

import bpy
import bmesh
from mathutils import Vector

wm = bpy.context.window_manager

# progress from [0 - 1000]


def symmetry_remesh(self):
    ob= bpy.context.active_object
    bpy.ops.object.modifier_add(type='MIRROR')
    bpy.context.object.modifiers["Mirror"].use_axis[0] = False
    bpy.context.object.modifiers["Mirror"].merge_threshold = bpy.context.scene.s_merge

    if bpy.context.object.s_axis == 'X':
        ob.modifiers["Mirror"].use_axis[0] = True
        ob.modifiers["Mirror"].use_bisect_axis[0] = True
    else:
        pass
    if bpy.context.object.s_axis == 'Y':
        ob.modifiers["Mirror"].use_axis[1] = True
        ob.modifiers["Mirror"].use_bisect_axis[1] = True
    else:
        pass
    if bpy.context.object.s_axis == 'Z':
        ob.modifiers["Mirror"].use_axis[2] = True
        ob.modifiers["Mirror"].use_bisect_axis[2] = True

    else:
        pass
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")





class RM_OT_relaxmethod(bpy.types.Operator):
    """Relax remesh object."""

    bl_idname = "object.remesh_relax"
    bl_label = "Remesh Relax"
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):

        bm = bmesh.new()
        bm.from_mesh(bpy.context.active_object.data)

        strength = bpy.context.scene.relax_strength
        tot = 50



        wm = bpy.context.window_manager
        for i in range(strength):
            wm.progress_begin(0, tot)
            for i in range(tot):
                wm.progress_update(i)

            for vert in bm.verts:
                avg = Vector()
                for edge in vert.link_edges:
                    other = edge.other_vert(vert)
                    avg += other.co
                avg /= len(vert.link_edges)
                avg -= vert.co
                avg -= avg.dot(vert.normal) * vert.normal
                vert.co += avg

        bm.normal_update()
        wm.progress_end()



        bm.to_mesh(bpy.context.active_object.data)



        bpy.context.active_object.data.update()

        bpy.context.view_layer.update()

        return {'FINISHED'}



def remesh_ff(self,context):
    bpy.ops.object.modifier_add(type='REMESH')
    bpy.context.object.modifiers["Remesh"].mode = 'SMOOTH'
    bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
    bpy.context.object.modifiers["Remesh"].scale = 1

    bpy.context.object.modifiers["Remesh"].octree_depth = bpy.context.scene.remesh_depth

    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

def density_ff(self,context):

    bpy.ops.object.mode_set(mode='SCULPT')
    bpy.ops.sculpt.dynamic_topology_toggle()
    bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE'

    bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'

    bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = bpy.context.scene.floodfill

    #bpy.ops.sculpt.optimize()
    bpy.context.view_layer.update()
    bpy.ops.sculpt.detail_flood_fill()




def dynamic_remesh(self,context):

    #progress bar


    ob = bpy.context.active_object

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    og_scale= bpy.context.object.scale

    dims = ob.dimensions
    x, y, z = bpy.context.active_object.dimensions

    if bpy.context.scene.keep_sculpt == True:
        bpy.ops.object.mode_set(mode='OBJECT')


    if bpy.context.object.mode == 'WEIGHT_PAINT':
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        pass

    ob = bpy.context.active_object
    original = bpy.data.objects[ob.name]



    scene = bpy.context.scene

    for ob in bpy.context.selected_objects:
        if ob.type == 'MESH' and ob.name.endswith("Remesh"):
            ob.select_set(True)
            bpy.ops.object.delete(use_global=False)
        else:
            pass

    ob = bpy.context.active_object
    ob.select_set(True)
    #bpy.ops.object.duplicate(linked=False)
    #bpy.context.object.scale = [15,15,15]
    ob.dimensions = 25.0, 25.0, 25.0

    bpy.ops.object.duplicate_move()


    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')




#    dims = bpy.context.object.dimensions
#    bpy.context.object.dimensions = 25.0, 25.0, 25.0




    #remesh_ff(self,context)


    #----------------------------




    density_ff(self,context)

    #----------------------------



    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')


    bpy.ops.mesh.vertices_smooth(factor=1)

    #bpy.ops.mesh.tris_convert_to_quads(face_threshold=3.14159, shape_threshold=3.14159)
    bpy.ops.object.mode_set(mode='OBJECT')


    target = original

    #DECIMATE MOD METHOD

    bpy.ops.object.modifier_add(type='DECIMATE')



    bpy.context.object.modifiers["Decimate"].ratio = bpy.context.scene.decimate
    bpy.context.object.modifiers["Decimate"].vertex_group = "vRemesh"
    bpy.context.object.modifiers["Decimate"].invert_vertex_group = True
    bpy.context.object.modifiers["Decimate"].vertex_group_factor = bpy.context.scene.d_factor
    bpy.context.object.modifiers["Decimate"].use_symmetry = True

    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')


    #bpy.ops.mesh.remove_doubles(threshold=1)
    #bpy.ops.mesh.vertices_smooth(factor=1)

    bpy.ops.mesh.tris_convert_to_quads(face_threshold=3.14159, shape_threshold=3.14159)
    bpy.ops.object.mode_set(mode='OBJECT')


    #bpy.ops.object.modifier_add(type='DISPLACE')
    #bpy.context.object.modifiers["Displace"].strength = bpy.context.scene.displace


    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.ops.object.modifier_add(type='SHRINKWRAP')

#


    ###############


    #bpy.ops.object.mode_set(mode='OBJECT')


    bpy.context.object.modifiers["Subdivision"].levels = bpy.context.scene.ccsubd

    bpy.context.object.modifiers["Shrinkwrap"].target = target
    bpy.context.object.modifiers["Shrinkwrap"].show_in_editmode = True
    bpy.context.object.modifiers["Shrinkwrap"].wrap_method = 'PROJECT'
    bpy.context.object.modifiers["Shrinkwrap"].use_negative_direction = True
    bpy.ops.object.modifier_add(type='SMOOTH')
    bpy.context.object.modifiers["Smooth"].factor = bpy.context.scene.smooth_factor
    bpy.context.object.modifiers["Smooth"].iterations = 1


    #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
    #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")





    if bpy.context.object.modifiers["Subdivision"].levels == 0:
        bpy.ops.object.modifier_remove(modifier="Subdivision")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")

    if bpy.context.object.modifiers["Smooth"].factor == 0:
        bpy.ops.object.modifier_remove(modifier="Smooth")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
    #bpy.ops.object.convert(target='MESH')

    bpy.context.object.name = bpy.context.object.name+"_Remesh"
    #bpy.ops.object.parent_clear(type='CLEAR')
    if bpy.context.scene.xray_mesh == True:

        bpy.context.object.show_in_front = True
        bpy.context.object.show_wire = True
        bpy.context.object.show_all_edges = True


    else:
        #bpy.context.object.display_type = 'WIRE'
        pass



    if bpy.context.scene.enable_sym == True:

        #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        symmetry_remesh(self)
    else:
        pass




    bpy.context.object.dimensions = x, y, z

    bpy.context.view_layer.objects.active = ob

    bpy.context.object.dimensions = x, y, z

    #ob.select_set(True)
    bpy.context.object.location= ob.location


            #bpy.ops.object.mode_set(mode='SCULPT')

    #bpy.ops.object.select_all(action='DESELECT')




    if bpy.context.scene.keep_sculpt == True:
        bpy.ops.object.mode_set(mode='SCULPT')

    else:
        pass



class QR_OT_remesh(bpy.types.Operator):
    """Quad-Remesh Dyntopo Model"""

    bl_idname = 'mesh.quadremesh'
    bl_label = "Remeshe Dyntopo Model with high number of tris."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #progress
#        wm = bpy.context.window_manager
#        tot =1000
#        wm.progress_begin(0, tot)
#
#        for i in range(tot):
#            wm.progress_update(i)



        dynamic_remesh(self,context)


        #wm.progress_end()
        return {'FINISHED'}

def update_decimate(self,context):


    if bpy.context.scene.auto_update == True:


        dynamic_remesh(self,context)


    else:
        pass

def update_presetsbar(self,context):
    if bpy.context.object.presets_bar == '0.005':
        bpy.context.scene.floodfill = 2.5
        bpy.context.scene.decimate = 0.009
        bpy.context.scene.ccsubd = 2
    else:
        pass

    if bpy.context.object.presets_bar == '0.05':
        bpy.context.scene.floodfill = 0.6
        bpy.context.scene.ccsubd = 2
        bpy.context.scene.decimate = 0.01
    else:
        pass
    if bpy.context.object.presets_bar == '0.1':
        bpy.context.scene.floodfill = 0.3
        bpy.context.scene.decimate = 0.1
        bpy.context.scene.ccsubd = 2
    else:
        pass

def update_subd(self,context):
    if bpy.context.scene.auto_update == True:

        dynamic_remesh(self,context)
    else:
        pass

def weightp(self,context):
    ob = bpy.context.active_object

    if ob.vertex_groups:
        pass
    else:

        bpy.ops.object.vertex_group_add()
    for vgroup in ob.vertex_groups:
        if vgroup.name.startswith("Group"):
            vgroup.name = "vRemesh"
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

class WP_OT_weightpaint(bpy.types.Operator):
    """Weight Paint Mode."""

    bl_idname = "object.wp_mode"
    bl_label = "WP_MODE"
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):

        weightp(self,context)

        return {'FINISHED'}

def oops(self, context):
    self.layout.label(text="Woah! Pretty dense model, try adding a Decimate Modifier, Lower Ratio, & Apply")



def recommend_op(self,context):
    ob = bpy.context.active_object
    obj = bpy.context.view_layer.objects.active
    data = obj.data
    total_triangles = 0
    for face in data.polygons:
        vertices = face.vertices
        triangles = len(vertices) - 2
        total_triangles += triangles
    print(total_triangles)
    #split = layout.split(factor=1)

    l = range(500,5000)
    if total_triangles in l:
        bpy.context.object.preset_indicator = 'L'

    m = range(5000,10000)
    if total_triangles in m:
        bpy.context.object.preset_indicator = 'M'




    h = range(10000,1000000)
    if total_triangles in h:

        bpy.context.object.preset_indicator = 'H'

def density_check(self, context):
    self.layout.label(text="Woah! This model is pretty dense, try adding a Decimate Modifier > Lower Ratio > Apply")



class ROP_OT_recommendop(bpy.types.Operator):
    """Recommended option."""

    bl_idname = "object.recommendop"
    bl_label = "Recommend Options"
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):
        ob = bpy.context.active_object
        obj = bpy.context.view_layer.objects.active
        data = obj.data
        total_triangles = 0
        for face in data.polygons:
            vertices = face.vertices
            triangles = len(vertices) - 2
            total_triangles += triangles
        print(total_triangles)

        h = range(100000,10000000)
        if total_triangles in h:
            bpy.context.window_manager.popup_menu(density_check, title="Suggestion", icon='ERROR')

        recommend_op(self,context)
        #self.report({'INFO'}, 'Printing report to Info window.')


        return {'FINISHED'}



bpy.types.Scene.decimate = bpy.props.FloatProperty(min = 0.0001, max = 1.0, default = 0.02, description="Decimate Factor: How much to decimate before remesh", update=update_decimate)
bpy.types.Scene.d_factor = bpy.props.FloatProperty(min = 0.0, max = 1000.0, default = 100.0, description="Decimate Factor: How much to decimate before remesh", update=update_decimate)
bpy.types.Scene.smooth_factor = bpy.props.FloatProperty(min = -2.0, max = 4.5, default = 1.0, description="Smoothing Factor: How much smoothness to apply after remesh", update=update_decimate)
bpy.types.Scene.ccsubd = bpy.props.IntProperty(min = 0, max = 6, default = 2, description="Times to subdivide after remesh", update=update_subd)
bpy.types.Scene.keep_sculpt = bpy.props.BoolProperty(name="keep_sculpt", default=False,description = "Keep sculpting mode enabled")
bpy.types.Scene.auto_update = bpy.props.BoolProperty(name="auto_update", default=False,description = "Auto-update settings when changing them.")
bpy.types.Scene.displace = bpy.props.FloatProperty(min = -10.0, max = 5.0, default = 1, description="Projection Factor", update=update_decimate)
bpy.types.Scene.xray_mesh = bpy.props.BoolProperty(name="xray_mesh", default=False,description = "Enable X-Ray.")
bpy.types.Scene.enable_sym = bpy.props.BoolProperty(name="enable_sym", default=False,description = "Enable Symmetry.")
bpy.types.Scene.s_merge = bpy.props.FloatProperty(min = 0.0, max = 0.2, default = 0.001, description="Symmetry Merge Limiit", update=update_decimate)
bpy.types.Scene.floodfill = bpy.props.FloatProperty(min = 0.02, max = 5.0, default = 0.5, description="Flood Fill Resolution", update=update_decimate)
bpy.types.Scene.relax_strength = bpy.props.IntProperty(min = 1, max = 50, default = 20, description="Relax strength value", update=None)
bpy.types.Scene.remesh_depth = bpy.props.IntProperty(min = 1, max = 8, default = 5, description="Remesh Depth", update=update_decimate)


class DR_PT_panel(bpy.types.Panel):

    bl_category = "Retopology"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "editmode"
    bl_label = "Retopology"


    def draw(self,context):

        layout = self.layout
        ob = bpy.context.active_object
        sculpt = context.tool_settings.sculpt


        if ob is not None:
            row = layout.split(align=True)
            row.prop(context.scene, "xray_mesh", text='', icon = 'HIDE_OFF')
            row.prop(context.scene, "auto_update",text='',icon= 'FILE_REFRESH')
            row.prop(context.scene, "keep_sculpt", text='',icon = 'SCULPTMODE_HLT')
            row.prop(context.scene, "enable_sym", text='', icon = 'UV_ISLANDSEL')


            row = layout.row(align=True)
            if bpy.context.scene.enable_sym == True:

                row.prop(ob, "s_axis", expand=True)
                row = layout.row(align=True)
                row.prop(context.scene, "s_merge",text="Merge Limit", slider=False)

            #layout = self.layout
            #split = layout.split(factor=1)

            col = layout.split(align=True,factor=1)

            col.operator("object.recommendop",text="Detect Polycount",icon = 'SHADERFX')
            col.scale_y = 1.4
            col = layout.split(align=True,factor=0.01)

            col.prop(ob, "preset_indicator", expand=True)



            col.prop(ob, "presets_bar", expand=True)
            col.scale_y = 1.4
            #if total_triangles == 3804:

            row = layout.row(align=True)
            row = row.column(align=True)
            row.operator("object.wp_mode",text="Weight Paint",icon = 'MOD_VERTEX_WEIGHT')
            row.prop(context.scene, "d_factor",text="Weight Factor", slider=False)
            #row.scale_y = 1.4
            #row = row.row(align=True)

            row.prop(context.scene, "floodfill",text="Density", slider=False)

            #row.prop(context.scene, "remesh_depth",text="Depth", slider=False)
            row.prop(context.scene, "decimate",text="Decimate", slider=False)
            row.scale_y = 1.7
            row = layout.row(align=True)
            row = row.column(align=True)
            row.prop(context.scene, "ccsubd",text="Subdivisions", slider=False)
            #row.prop(context.scene, "displace",text="Relax", slider=False)

            row.prop(context.scene, "smooth_factor",text="Smoothness", slider=False)


            row.prop(context.scene, "relax_strength",text="Relax Strength", slider=True)
            row.operator("object.remesh_relax",text="Relax",icon = 'MESH_GRID')
            row.scale_y = 1.7
            row = layout.row(align=True)


            row = layout.row(align=True)
            row.operator(QR_OT_remesh.bl_idname, text="Remesh", icon = 'MOD_REMESH')
            row.scale_y = 2.0
#            if (sculpt.detail_type_method == 'CONSTANT'):
#                row.prop(sculpt, "constant_detail_resolution")
#                row.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')

        else:
            layout = self.layout
            layout.label(text="Select your model first", icon = 'URL')
            layout.scale_y = 2.0
classes = ( QR_OT_remesh, WP_OT_weightpaint,ROP_OT_recommendop,RM_OT_relaxmethod, DR_PT_panel)
def register():
    #bpy.utils.register_module(__name__)
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Object.s_axis = bpy.props.EnumProperty(
    name="Axis",
    description="Symmetry Axis",

    items=[("X","X","X-axis",'',0),

           ("Y","Y","Y-axis",'',1),
           ("Z","Z","Z-axis",'',2)

          ],
          default= None,
          update= update_decimate

          #options= {'ENUM_FLAG'},
          )

    bpy.types.Object.presets_bar = bpy.props.EnumProperty(
    name="Preset Bar",
    description="Preset Bar: Recommends settings depending on your models poly count.",

    items=[("0.005","High","High Polycount",'',0),

           ("0.05","Medium" ,"Medium Polycount",'',1),
           ("0.1","Low","Low Polycount",'',2)

          ],
          default= '0.1',
          update= update_presetsbar,

          #options= {'ENUM_FLAG'},
          )

    bpy.types.Object.preset_indicator= bpy.props.EnumProperty(
    name="Preset Indicator",
    description="Preset Indicator: Recommends settings depending on your models poly count.",

    items=[("H","","High Polycount",'',0),

           ("M","","Medium Polycount",'',1),
           ("L","","Low Polycount",'',2)

          ],
          default= 'L',
          update= None,

          options= {'HIDDEN'},
          )


    bpy.types.Scene.decimate = bpy.props.FloatProperty(min = 0.0001, max = 1.0, default = 0.02, description="Decimate Factor: How much to decimate before remesh", update=update_decimate)
    bpy.types.Scene.d_factor = bpy.props.FloatProperty(min = 0.0, max = 1000.0, default = 100.0, description="Weight Factor: Density on painted weight", update=update_decimate)
    bpy.types.Scene.smooth_factor = bpy.props.FloatProperty(min = -2.0, max = 4.5, default = 1.0, description="Smoothing Factor: How much smoothness to apply after remesh", update=update_decimate)
    bpy.types.Scene.ccsubd = bpy.props.IntProperty(min = 0, max = 6, default = 2, description="Subdivisions after remesh", update=update_subd)
    bpy.types.Scene.keep_sculpt = bpy.props.BoolProperty(name="keep_sculpt", default=False,description = "Keep sculpting mode enabled")
    bpy.types.Scene.auto_update = bpy.props.BoolProperty(name="auto_update", default=False,description = "Auto-update settings when changing them.")
    bpy.types.Scene.displace = bpy.props.FloatProperty(min = -10.0, max = 5.0, default = 1, description="Projection Factor", update=update_decimate)
    bpy.types.Scene.xray_mesh = bpy.props.BoolProperty(name="xray_mesh", default=False,description = "Enable X-Ray.")
    bpy.types.Scene.enable_sym = bpy.props.BoolProperty(name="enable_sym", default=False,description = "Enable Symmetry.")
    bpy.types.Scene.s_merge = bpy.props.FloatProperty(min = 0.0, max = 0.2, default = 0.001, description="Symmetry Merge Limiit", update=update_decimate)
    bpy.types.Scene.floodfill = bpy.props.FloatProperty(min = 0.02, max = 5.0, default = 0.5, description="Flood Fill Resolution", update=update_decimate)
    bpy.types.Scene.relax_strength = bpy.props.IntProperty(min = 1, max = 50, default = 20, description="Relax strength value", update=None)
    bpy.types.Scene.remesh_depth = bpy.props.IntProperty(min = 1, max = 8, default = 5, description="Remesh Depth", update=update_decimate)


def unregister():
    #bpy.utils.unregister_module(__name__)
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
