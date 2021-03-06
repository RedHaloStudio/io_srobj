	
import bpy
import mathutils
import math
from string import *
from struct import *
from math import *
from bpy.props import *
from bpy_extras.io_utils import ImportHelper

def objimport(path):
	
	meshname = ''
	verts = []
	faces = []
	groupnames = []
	vertgroups = []
	groupedverts = []
	facenormals = []
	faceUv = []
	uv = []
	normals = []
	groupnames = []
	vertgroups = []
	
	file = open(path, 'r')
	for line in file:
		words = line.split()
		if len(words) == 0 or words[0].startswith('#'):
			pass
		elif words[0] == 'o':
			meshname = words[1]
		elif words[0] == 'v':
			x, z, y = float(words[1]), float(words[2]), float(words[3])
			verts.append([x, -1*y, z])
		elif words[0] == 'vn':
			x, z, y = float(words[1]), float(words[2]), float(words[3])
			normals.append([y,x,z])
		elif words[0] == 'vt':
			u, v = float(words[1]), float(words[2])
			uv.append([u,v])
		elif words[0] == 'gn':
			groupnames.append(line.replace('gn ','')[:-1])
		elif words[0] == 'vg':
			values = words[1].split('/')
			vertgroups.append([int(values[0]),int(values[1])])
		elif words[0] == 'f':
			faceVertList = []
			facenormals.append(int(words[1].split('/')[2])-1)
			faceUvList = []
			for faceIdx in words[1:]:
				faceVert = (int(faceIdx.split('/')[0])-1)
				uvI = (int(faceIdx.split('/')[1])-1)
				faceVertList.append(faceVert)
				faceUvList.append(uvI)
			faces.append(faceVertList)
			faceUv.append(faceUvList)
	
	# link the mesh to a new object
	if nameExists(meshname) != 0:
		meshname += '.'+str(nameExists(meshname))
	
	mesh = bpy.data.meshes.new(meshname)
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	
	for index, face in enumerate(faces):
		for vert in face:
			mesh.vertices[vert].normal = normals[facenormals[index]]
	
	mesh.uv_layers.new()
	
	for i, uvs in enumerate(faceUv):
		mesh.uv_layers.active.data[i*3].uv = uv[uvs[0]]
		mesh.uv_layers.active.data[i*3+1].uv = uv[uvs[1]]
		mesh.uv_layers.active.data[i*3+2].uv = uv[uvs[2]]
	
	mesh.update()
	
	profile_object = bpy.data.objects.new(meshname, mesh)  
	profile_object.data = mesh
	
	for names in groupnames:
		groupedverts.append([])
	
	for i, groups in enumerate(vertgroups):
		if groups[0] != 255:
			groupedverts[groups[0]].append(i)
		if groups[1] != 255:
			groupedverts[groups[1]].append(i)
	
	for i, group in enumerate(groupnames):
		vgroup = profile_object.vertex_groups.new(name = group)
		vgroup.add(groupedverts[i], 0, 'ADD')
	
	for i, vert in enumerate(profile_object.data.vertices):
		for j, group in enumerate(profile_object.data.vertices[i].groups):
			profile_object.data.vertices[i].groups[j].weight = 1

	bpy.context.collection.objects.link(profile_object)
	profile_object.select_set(True)

def nameExists(name):
	exist = 0
	for object in bpy.context.scene.objects:
		if object.name == name:
			exist += 1

	return exist
	
def getInputFilename(self,filename):
	checktype = filename.split('\\')[-1].split('.')[-1]
	print ("------------",filename)
	if checktype.lower() != 'srobj':
		print ("  Selected file = ",filename)
		raise (IOError, "The selected input file is not a *.srobj file")
	else:
		objimport(filename)
		
# class IMPORT_OT_psk(bpy.types.Operator):
class IMPORT_OT_psk(bpy.types.Operator, ImportHelper):
	'''Load a skeleton mesh psk File'''
	bl_idname = "import_scene.srobj"
	bl_label = "Import SROBJ"
	# bl_space_type = "PROPERTIES"
	# bl_region_type = "WINDOW"

	filename_ext = ".srobj"
	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	filepath = StringProperty(
			name="File Path",
			description="Filepath used for importing the srobj file",
			maxlen= 1024,
			subtype='FILE_PATH',
		)
	filter_glob = StringProperty(
			default="*.srobj",
			options={'HIDDEN'},
		)

	def execute(self, context):
		getInputFilename(self,self.filepath)
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}  

def menu_func(self, context):
    self.layout.operator(IMPORT_OT_psk.bl_idname, text="Silkroad Object (.srobj)")

def register():
	bpy.utils.register_class(IMPORT_OT_psk)
	bpy.types.TOPBAR_MT_file_import.append(menu_func)

def unregister():
	bpy.utils.unregister_class(IMPORT_OT_psk)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func)

if __name__ == "__main__":
	register()