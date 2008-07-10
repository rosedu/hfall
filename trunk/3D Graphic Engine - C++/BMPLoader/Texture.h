#ifndef TEXTURE
#define TEXTURE

namespace Engine
{
	class Texture
	{
		protected:
			char *filename;
			unsigned char *texture;
			int width,height;
		public:
			Texture();
			Texture(char *filename);
			virtual ~Texture();
			virtual bool load();
			int getHeight();
			int getWidth();
			unsigned char* data();
	};
}

#endif
