#include "Texture.h"
#include <stdlib.h>
#include<string.h>

using namespace Engine;

Texture::Texture() {}
Texture::Texture(char *name)
{
	filename = (char *) malloc(25*sizeof(char));
	strcpy(filename,name);
}
Texture::~Texture() {}
unsigned char *Texture::data()
{
	return texture;
}
int Texture::getHeight() { return height; }
int Texture::getWidth() { return width; }
bool Texture::load() { return false; }
