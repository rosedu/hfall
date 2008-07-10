#ifndef BMPTEXTURE
#define BMPTEXTURE

#include "Texture.h"
namespace Engine
{
	class BMPTexture: public Texture
	{
		public:
			BMPTexture(char *filename);
			~BMPTexture();
			bool load();
			bool loadToVRAM();
	};
}

#endif
