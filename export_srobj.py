import bpy
import mathutils
import math
from string import *
from struct import *
from math import *
from bpy.props import *
from bpy_extras.io_utils import ExportHelper

def objexport(path):
	obj = bpy.context.object
	if obj.type != 'MESH':
		raise(IOError, 'You must select the mesh')
	else:
		meshname = ''
		groupnames = []
		vertgroups = []
		verts = []
		normals = []
		uv = []
		faces = []

		meshname = obj.name
		mesh = obj.data
		tex = mesh.uv_layers.active
		
		for vert in obj.data.vertices:
			verts.append(vert.co.xzy)
			uv.append([])
			groups = []
			for g in vert.groups:
				groups.append(g.group)
			vertgroups.append(groups)
		
		for face in mesh.polygons:
			faces.append(face.vertices)
			normals.append(mesh.vertices[face.vertices[0]].normal)

		for i, texface in enumerate(tex.data):
			uv[faces[math.floor(i/3)][i%3]] = texface
		
		for group in obj.vertex_groups:
			groupnames.append(group.name)
		
		lines = []
		
		lines.append('#SROBJ by Perry\'s Blender plugin.'+'\n')
		lines.append('o '+meshname+'\n')
		
		for groupname in groupnames:
			lines.append('gn '+ groupname +'\n')
		
		for groups in vertgroups:
			if len(groups) == 1:
				groups.append(255)

			if len(groups) > 0:
				v = groups[0]
				v2 = groups[1]

			lines.append('vg ' + str(v)+'/' + str(v2) + '\n')
			
		for vert in verts:
			lines.append('v '+str(vert[0])+' '+str(vert[1])+' '+str(vert[2]*-1)+'\n')
			
		for norm in normals:
			lines.append('vn '+str(norm[0])+' '+str(norm[2])+' '+str(norm[1])+'\n')
		
		for coords in uv:
			lines.append('vt '+str(coords.uv[0])+' '+str(coords.uv[1])+'\n')
			
		for i, face in enumerate(faces):
			lines.append('f '+str(face[0]+1)+'/'+str(face[0]+1)+'/'+str(i+1)+' '+str(face[1]+1)+'/'+str(face[1]+1)+'/'+str(i+1)+' '+str(face[2]+1)+'/'+str(face[2]+1)+'/'+str(i+1)+'\n')
		
		f = open(path, 'w')
		f.writelines(lines)
		f.close()
		
def getInputFilename(self,filename):
	checktype = filename.split('\\')[-1][-6:]
	print ("------------",filename)
	if checktype.lower() != '.srobj':
		objexport(filename+'.srobj') 
		#self.report({'INFO'}, ("Selected file:"+ filename))
	else:
		objexport(filename)
		
class EXPORT_OT_psk(bpy.types.Operator, ExportHelper):
	'''Load a skeleton mesh psk File'''
	bl_idname = "export_scene.srobj"
	bl_label = "Export SROBJ"

	filename_ext = ".srobj"
	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	filepath = StringProperty(
			name="File Path",
			description="Filepath used for importing the srobj file",
			maxlen= 1024,
			subtype='FILE_PATH',
			)

	def execute(self, context):
		getInputFilename(self,self.filepath)
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}  

def menu_func(self, context):
	self.layout.operator(EXPORT_OT_psk.bl_idname, text="Silkroad Object (.srobj)")

def register():
	bpy.utils.register_class(EXPORT_OT_psk)
	bpy.types.TOPBAR_MT_file_export.append(menu_func)
	
def unregister():
	bpy.utils.unregister_class(EXPORT_OT_psk)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
	register()