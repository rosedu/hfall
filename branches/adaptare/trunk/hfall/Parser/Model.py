import sys
sys.path.insert(0,"../")
sys.path.insert(0,"../Engine")
sys.path.insert(0,"../UI")
import base
from Vector import *
import struct

MESH_CHUNK = 0x10
VERTEX_CHUNK = 0x20
TRIANGLE_CHUNK = 0x30
NORMAL_CHUNK = 0x40
UV_CHUNK = 0x50
TEXTURE_CHUNK = 0x60
JOINT_CHUNK = 0x70
VERTEX_JOINT_CHUNK = 0x71
SIZE_INT = 4
SIZE_FLOAT = 4
SIZE_CHAR = 4


def Joint_SetInitialRotation(self,alph,beta,theta):
    pass


def Model_Render(self):
    aa"""Render a model"""
    #print len(self._meshes),"<"
    rnd = open("RENDER","w")
        
    for msh in self._meshes:

        i = 0
        for tr in msh._triangles:
            rnd.write("Triangle %d:\n"%(i,))
            #print tr._vertices,"VER"
            rnd.write("Vertex 1 (%d):\n"%tr._vertices[0])
            rnd.write("%f %f %f\n"%(msh._vertices[tr._vertices[0]].position.x,msh._vertices[tr._vertices[0]].position.y,msh._vertices[tr._vertices[0]].position.z))
            rnd.write("Vertex 2 (%d):\n"%tr._vertices[1])
            rnd.write("%f %f %f\n"%(msh._vertices[tr._vertices[1]].position.x,msh._vertices[tr._vertices[1]].position.y,msh._vertices[tr._vertices[1]].position.z))
            rnd.write("Vertex 3 (%d):\n"%tr._vertices[2])
            rnd.write("%f %f %f\n"%(msh._vertices[tr._vertices[2]].position.x,msh._vertices[tr._vertices[2]].position.y,msh._vertices[tr._vertices[2]].position.z))
                
            glBegin(GL_TRIANGLES)
            glVertex3f(
                msh._vertices[tr._vertices[0]].position.x,
                msh._vertices[tr._vertices[0]].position.y,
                msh._vertices[tr._vertices[0]].position.z
            )
            
            glVertex3f(
                msh._vertices[tr._vertices[1]].position.x,
                msh._vertices[tr._vertices[1]].position.y,
                msh._vertices[tr._vertices[1]].position.z
            )
            glVertex3f(
                msh._vertices[tr._vertices[2]].position.x,
                msh._vertices[tr._vertices[2]].position.y,
                msh._vertices[tr._vertices[2]].position.z
            )
                
            glEnd()
            i+=1        
    rnd.close()    

def Model_SetNumMeshes(self,num_meshes):
    pass


def Model_SetNumJoints(self,num_joints):
    pass


def Model_GetNumJoints(self):
    pass


def Set_InitialRotations(self):
    pass

def Set_InitialTranslations(self):
    pass

def Model_Load(self,file_name):
    f_in = open(file_name,"r")
    in_buffer = f_in.read(1)
    in_buffer = f_in.read(1)
    c_id = ord(in_buffer[0])
    if c_id!=MESH_CHUNK:
        print "file corupted:mesh chunk id does not match"
    in_buffer = f_in.read(SIZE_INT);
    print struct.unpack("i",in_buffer)[0]
    num_meshes = struct.unpack("i",in_buffer)[0]
    print "num_meshes", num_meshes
    dbg = open("DBG","w")
    for i in range(num_meshes):
        print "MESH", i
        print i, len(self._meshes)
        mesh = Mesh()
        #read the chunk id
        in_buffer = f_in.read(1)
        c_id = ord(in_buffer[0])
        if c_id != TEXTURE_CHUNK:
            print "file corupted:texture chunk id does not match ",c_id
        
        #read the number of textures
        in_buffer = f_in.read(SIZE_INT)
        print ord(in_buffer[1]),ord(in_buffer[2]),ord(in_buffer[3])
        tex_num = struct.unpack("i",in_buffer)[0]
        print "tex_num",tex_num
        for j in range(tex_num):
            #read the length of the string
            in_buffer = f_in.read(SIZE_INT)
            name_len = struct.unpack("i",in_buffer)[0]
            #read it from the file
            t_string = f_in.read(name_len)
            print t_string
            #texture_handle t_handle;
            #t_handle = m_tex_manager.loadTGA(t_string);
            
            #mesh.AddTexture(t_handle,0);
           
        in_buffer = f_in.read(1)
        c_id = ord(in_buffer[0])
        if c_id!=VERTEX_CHUNK:
            print "file corupted:vertex chunk id does not match"

        in_buffer = f_in.read(SIZE_INT)
        vertex_num = struct.unpack("i",in_buffer)[0]
        t_x = []
        t_y = []
        t_z = []

        for j in range(vertex_num):
            dbg.write("VERTEX %d\n"%(j,))
            in_buffer = f_in.read(SIZE_FLOAT);
            print len(in_buffer)
            t_x.append(struct.unpack("f",in_buffer)[0])
            in_buffer = f_in.read(SIZE_FLOAT);
            t_y.append(struct.unpack("f",in_buffer)[0])
            in_buffer = f_in.read(SIZE_FLOAT);
            t_z.append(struct.unpack("f",in_buffer)[0])
            dbg.write("%f %f %f\n"%(t_x[-1],t_y[-1],t_z[-1]))
        print t_x        
        mesh.SetVertices(t_x,t_y,t_z);
        
        #read triangle chunk ID
        in_buffer = f_in.read(1)
        c_id = ord(in_buffer[0])
        if c_id!=TRIANGLE_CHUNK: 
            print "file corupted: triangle chunk id does not match"

        in_buffer = f_in.read(SIZE_INT);

        triangle_num = struct.unpack("i",in_buffer)[0]
        triang = []
        for j in range(triangle_num):
            vert  = []
            in_buffer = f_in.read(SIZE_INT)
            vert.append(  struct.unpack("i",in_buffer)[0])
            in_buffer = f_in.read(SIZE_INT)
            vert.append(  struct.unpack("i",in_buffer)[0])
            in_buffer = f_in.read(SIZE_INT)
            vert.append(  struct.unpack("i",in_buffer)[0])
            triang.append(vert)
           
        mesh.SetTriangles(triang)
         
        in_buffer = f_in.read(1)
        c_id = ord(in_buffer[0])
        if c_id != NORMAL_CHUNK:
            print "file corupted:normal chunk id does not match"

        in_buffer = f_in.read(SIZE_INT)
        normal_num = struct.unpack("i",in_buffer)[0]
        t_triang = []
        for j in range(normal_num):
            in_buffer = f_in.read(SIZE_FLOAT);
            t_x[j] = struct.unpack("f",in_buffer)[0]
            in_buffer = f_in.read(SIZE_FLOAT);
            t_y[j] = struct.unpack("f",in_buffer)[0]
            in_buffer = f_in.read(SIZE_FLOAT);
            t_z[j] = struct.unpack("f",in_buffer)[0]
            
        #mesh.AddNormals(normal_num, t_x, t_y, t_z);
        t_n = []
        for j in range(triangle_num):
            in_buffer = f_in.read(3*SIZE_INT);
            t_n.append (Vector3(
                struct.unpack("i",in_buffer[0:SIZE_INT])[0],
                struct.unpack("i",in_buffer[SIZE_INT:2*SIZE_INT])[0],
                struct.unpack("i",in_buffer[2*SIZE_INT:3*SIZE_INT])[0])
            )
               
        #mesh.SetNormals(t_n)
                

        in_buffer = f_in.read(1);
        c_id = ord(in_buffer[0])
        if c_id != UV_CHUNK:
            print "file corupted:UV chunk id does not match"
        
        t_u = []
        t_v = []
        for j in range(vertex_num):
            in_buffer = f_in.read(SIZE_FLOAT);
            t_u.append(struct.unpack("i",in_buffer)[0])
            in_buffer = f_in.read(SIZE_FLOAT);
            t_v.append(struct.unpack("i",in_buffer)[0])
               
            
        #mesh.SetUV(t_u, t_v);
        #read the vertex-joint associations
        in_buffer = f_in.read(1)
        c_id = ord(in_buffer[0])
        if c_id != VERTEX_JOINT_CHUNK:
            print "file corupted:vertex-joint association chunk id does not match"
            
        t_joint = []
        print "VERTEX_NUM", vertex_num
        for j in range(vertex_num):
            in_buffer = f_in.read( SIZE_INT);
            t_joint.append(struct.unpack("i",in_buffer)[0])
            
        #mesh.AssignJoints(vertex_num, t_joint);
        
        self._meshes.append(mesh)
         
    in_buffer = f_in.read(1);
    c_id = ord(in_buffer[0])
    dbg.close()
    if c_id != JOINT_CHUNK:
        print "file corupted:joint chunk id does not match"
    in_buffer = f_in.read(SIZE_INT);
    num_joints = struct.unpack("i",in_buffer)[0]
    for i in range(num_joints):
             #read and set the jonint`s rotation      
        in_buffer = f_in.read(3*SIZE_FLOAT);
     #        self._joints.append()
     #        self._joints[i].SetInitialRotation(
     #           struct.unpack("f",in_buffer)[0],
     #           struct.unpack("f",in_buffer)[1],
     #           struct.unpack("f",in_buffer)[2]
     #        )
                    
             #and translation
        in_buffer = f_in.read(3*SIZE_FLOAT)
     #        self._joints[i].SetInitialRotation(
     #           struct.unpack("f",in_buffer)[0],
     #           struct.unpack("f",in_buffer)[1],
     #           struct.unpack("f",in_buffer)[2]
     #        )
                    
        in_buffer = f_in.read(SIZE_FLOAT);
     #        self._joints[i].SetParent(struct.unpack("i",in_buffer)[0])
             
                    
class Quaternion:
    pass


class Vertex:
    def __init__(self,x,y,z):
        self.position = Vector3(x,y,z)
    def SetJoint(self,p_joint):
        self._joints[0] = p_joints
        self._weights[0] = 1
    position = Vector3()
    _joints = []
    _weigths = []
    _normal = Vector3()
  
    

class Triangle:
    def __init__(self, p_vertices):
        self._vertices = []
        for vert in p_vertices:
            self._vertices.append(vert)
            
        print self._vertices,"v"
    def SetVertices(self,p_vertices):
        for vert in p_vertices:
            self._vertices.append(vert)
    def SetUV(self,u,v):
        self._uv.x = u
        self._uv.y = v
    _vertices = []
    _uv = Vector2()

class Material:
    pass


class Joint:
    #methods    
    def SetInitialRotation(self,p_init):
        self._initial_rotation = p_init
    def SetAbsInitialRotation(self,p_init):
        self._abs_initial_rotation = p_init
    def SetRotation(self,p_rot):
        self._rotation = p_rot
    def SetInitialTranslation(self,p_init):
        self._initial_translation = p_init
    def SetAbsInitialTranslation(self,p_init):
        self._abs_initial_translation = p_init
    def SetTranslation(self,p_trans):
        self._translation = p_trans

    #members
    _initial_rotation = Quaternion()
    _abs_initial_rotation = Quaternion()
    _rotation = Quaternion 
    _initial_translation = Vector3()
    _abs_initial_translation = Vector3() 
    _translation = Vector3()
    


class Mesh:
    #methods
    def SetVertices(self,p_x,p_y,p_z):
        self._vertices = []
        print len(p_x)
        for i in range(len(p_x)):
            self._vertices.append(Vertex(p_x[i],p_y[i],p_z[i]))

    def SetTriangles(self,p_triangles):
        self._triangles = []
        for tr in p_triangles:
            self._triangles.append(Triangle(tr))
        for i in self._triangles:
            #print i._vertices," < "
            pass

    def SetNormals(self,p_normals):
        self._normals = p_normals

    def SetUV(self, t_u, t_v):
        for i in range(len(self._vertices)):
            _vertices[i].SetUV(t_u,t_v)

    def AssignJoints(self,vertex_num, t_joint):
        for i in range(len(self._vertices)):
            self._vertices[i].SetJoint(t_joint[i])
    #members
    _vertices = []
    _triangles = []
    _normals = []
    _material = None


class Model:
    def __init__(self):
        self._meshes = []
    #methods    
    Load = Model_Load
    Render = Model_Render 
    #members
    _meshes = []
    _filename = None
    _joints = []
    
class Model_Instance:
    #methods
    Render = Model_Render
    #members