#ifndef _MESH_
#define _MESH_

#include "Matrix4.h"
#include "Material.h"
#include "Vertex.h"
#include "Array.h"

namespace Engine
{
	class Mesh
	{
		public:
			Mesh();
			~Mesh();
			
		private:
			char *name;
			Array<Vertex> vertices;
			Array<Vector3h> faces;
			Array<MeshMaterialGroup> groups;
			Matrix4f matrix;
	};
	
	class MeshMaterialGroup
	{
		friend class Mesh;
		
		private:
			Material material;
			Array<unsigned short> faces;
	};
}

#endif
