import bpy
import bmesh
import math

class REFYNE_OT_start_modeling(bpy.types.Operator):
    """Creates a new project for modeling clothes"""
    bl_idname = "refyne.start_modeling"
    bl_label = "Start Modeling"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'OBJECT'

    def execute(self, context):
        
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, location=(0, 0, 0))
        bpy.context.active_object.name = 'clothes_project'
        bpy.context.object.data.dimensions = '2D'
        bpy.ops.curve.spline_type_set(type='POLY')

        return {'FINISHED'}

class REFYNE_OT_create_segment(bpy.types.Operator):
    """Joins curves with a new segement"""
    bl_idname = "refyne.create_segment"
    bl_label = "Create Segment"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):

        try:
            bpy.ops.curve.make_segment()
        except RuntimeError as ex:
            error_report = "\n".join(ex.args)
            self.report({'ERROR'}, error_report)
            return {'CANCELLED'}

        return {'FINISHED'}

class REFYNE_OT_linear_spline(bpy.types.Operator):
    """Sets a linear spline type"""
    bl_idname = "refyne.linear_spline"
    bl_label = "Linear Spline"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):

        bpy.ops.curve.spline_type_set(type='POLY')
            
        return {'FINISHED'}

class REFYNE_OT_curved_spline(bpy.types.Operator):
    """Sets a curved spline type"""
    bl_idname = "refyne.curved_spline"
    bl_label = "Curved Spline"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):

        bpy.ops.curve.spline_type_set(type='BEZIER')
            
        return {'FINISHED'}

class REFYNE_OT_create_plane(bpy.types.Operator):
    """Creates a plane from selected curves"""
    bl_idname = "refyne.create_plane"
    bl_label = "Create Plane"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'EDIT_CURVE'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        try:
            bpy.ops.mesh.fill_grid()
        except RuntimeError as ex:
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            obj = bpy.context.active_object
            obj.data.edges[0].select = True
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.subdivide()
            bpy.ops.mesh.select_all(action='SELECT')
            try:
                bpy.ops.mesh.fill_grid()
            except RuntimeError as ex2:
                error_report = "\n".join(ex.args)
                self.report({'ERROR'}, error_report)
                return {'CANCELLED'}
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_add(type='CLOTH')
        bpy.context.object.modifiers["Cloth"].settings.effector_weights.gravity = 0
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}