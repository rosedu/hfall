#ifndef _TEXTURE_
#define _TEXTURE_

#include "Color.h"

class Texture
{
	public:
		Texture();
		Texture(char *filename);
		~Texture();
		
	private:
		int id;
		char *name;
		unsigned short percentage;
		unsigned short bump_percent;
		unsigned short tiling;
		float blur;
		float u_scale;
		float v_scale;
		float u_offset;
		float v_offset;
		float rotation_angle;
		Color first_blend;
		Color second_blend;
		Color red_blend;
		Color green_blend;
		Color blue_blend;
};

#endif
