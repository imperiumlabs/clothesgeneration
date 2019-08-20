import bpy

def view3d_find( return_area = False ):
    # Returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    if return_area: return region, rv3d, v3d, area
                    return region, rv3d, v3d
    return None, None

class REFYNE_OT_sew(bpy.types.Operator):
    """Sews two edges together"""
    bl_idname = "refyne.sew"
    bl_label = "Sew"
    bl_options = {'REGISTER', 'UNDO'}

    stitches = bpy.props.IntProperty(default = 2, min = 2, max = 50)

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'EDIT_MESH'

    def execute(self, context):

        # Setup
        region, rv3d, v3d, area = view3d_find(True)
        override = {
        'scene'  : bpy.context.scene,
        'region' : region,
        'area'   : area,
        'space'  : v3d
        }
        bpy.ops.object.editmode_toggle()
        obj = bpy.context.active_object
        num_stitches = self.stitches - 2
        num_edges = len([e for e in bpy.context.active_object.data.edges])
        selected_edge_indices = [e.index for e in bpy.context.active_object.data.edges if e.select]
        # Preps mesh for sewing
        bpy.ops.object.editmode_toggle()
        if num_stitches != 0:
            for selected_edge_index in selected_edge_indices:
                bpy.ops.mesh.select_all(action = 'DESELECT')
                bpy.ops.object.editmode_toggle()
                obj.data.edges[selected_edge_index].select = True
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.subdivide(number_cuts=num_stitches)
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.editmode_toggle()
        for x in range(num_edges, num_edges + num_stitches*len(selected_edge_indices)):
            obj.data.edges[x].select = True
        for x in selected_edge_indices:
            obj.data.edges[x].select = True
        # Sews vertices
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.bridge_edge_loops()
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_add(type='CLOTH')
        bpy.context.object.modifiers["Cloth"].settings.effector_weights.gravity = 0
        bpy.context.object.modifiers["Cloth"].settings.use_sewing_springs = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type="EDGE")

        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
