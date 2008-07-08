#ifndef _MATERIAL_
#define _MATERIAL_

#include "Color.h"
#include "Texture.h"

namespace Engine
{
	class Material
	{
		public:
			Material();
			~Material();
			
		private:
			char *name;
			Color ambient;
			Color diffuse;
			Color specular;
			unsigned short shininess_ratio;
			unsigned short shininess_strength;
			unsigned short transparency;
			unsigned short refelection_blur;
			unsigned short shading_type;
			Texture texture_map;
			Texture specular_map;
			Texture opacity_map;
			Texture reflection_map;
			Texture bump_map;
			Texture shininess_map;
			Texture texture_mask;
			Texture specular_mask;
			Texture opacity_mask;
			Texture reflection_mask;
			Texture bump_mask;
			Texture shininess_mask;
			float wire_size;
			bool wireframe;
			bool two_sided_lighting;
	};
}

#endif
