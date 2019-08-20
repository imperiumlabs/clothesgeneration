import bpy

class REFYNE_PT_main(bpy.types.Panel):
    bl_label = "Clothes Modeling"
    bl_idname = "REFYNE_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Blueprints
        # layout.label(text="Blueprints:")
        # row = layout.row() 
        # row.template_list("REFYNE_UL_blueprints", "", scene, "blueprint_list", scene, "blueprint_list_index")
        # row = layout.row() 
        # row.operator('refyne.add_blueprint', text='Add Blueprint') 
        # row.operator('refyne.remove_blueprint', text='Remove Blueprint')
        # if scene.blueprint_list_index >= 0 and scene.blueprint_list:
        #     item = scene.blueprint_list[scene.blueprint_list_index]
        #     row = layout.row() 
        #     row.prop(item, "name") 
        #     row.prop(item, "random_property")

        # Modeling
        layout.label(text="Modeling:")
        row = layout.row()
        row.operator("refyne.start_modeling")
        row = layout.row()
        row.operator("refyne.create_segment")
        row = layout.row()
        row.operator("refyne.linear_spline")
        row = layout.row()
        row.operator("refyne.curved_spline")
        row = layout.row()
        row.operator("refyne.create_plane")

        # Human
        layout.label(text="Human:")
        row = layout.row()
        row.operator("refyne.import_human")

        # Sewing
        layout.label(text="Sewing:")
        row = layout.row()
        row.operator("refyne.sew")

        # Rendering
        layout.label(text="Rendering:")
        row = layout.row()
        row.operator("refyne.render")
        row = layout.row()
        row.prop(scene, "tension_map")

        # sub = row.row()
        # sub.scale_x = 2.0
        # sub.operator("render.render")

        # row.operator("render.render")

        # # Create a simple row.
        # layout.label(text=" Simple Row:")

        # row = layout.row()
        # row.prop(scene, "frame_start")
        # row.prop(scene, "frame_end")

        # # Create an row where the buttons are aligned to each other.
        # layout.label(text=" Aligned Row:")

        # row = layout.row(align=True)
        # row.prop(scene, "frame_start")
        # row.prop(scene, "frame_end")

        # # Create two columns, by using a split layout.
        # split = layout.split()

        # # First column
        # col = split.column()
        # col.label(text="Column One:")
        # col.prop(scene, "frame_end")
        # col.prop(scene, "frame_start")

        # # Second column, aligned
        # col = split.column(align=True)
        # col.label(text="Column Two:")
        # col.prop(scene, "frame_start")
        # col.prop(scene, "frame_end")

        # # Big render button
        # layout.label(text="Big Button:")
        # row = layout.row()
        # row.scale_y = 3.0
        # row.operator("render.render")


