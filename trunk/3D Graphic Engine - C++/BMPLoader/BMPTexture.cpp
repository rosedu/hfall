#include "bitmap.h"
#include "BMPTexture.h"
#include <GL/glut.h>
#include <iostream>
#include <string.h>
#include <stdlib.h>

using namespace Engine;

BMPTexture::BMPTexture(char *fname) : BMPTexture::Texture(fname) {}
BMPTexture::~BMPTexture() {}
bool BMPTexture::load()
{
	BITMAPFILEHEADER fileheader;
	BITMAPINFOHEADER infoheader;
	BMPCOLOR pixel;
	if(!strstr(filename,".bmp"))
	{
		std::cout << "Invalid source file extension\nExtension must be .bmp\n";
		return false;
	}
	FILE *f=fopen(filename,"rb");
	if(!f)
	{
		std::cout << "No file" << filename << "\n";
		return false;
	}
	int k=fread(&fileheader,sizeof(BITMAPFILEHEADER),1,f);
	int l=fread(&infoheader,sizeof(BITMAPINFOHEADER),1,f);
	if(!k || !l)
	{
		std::cout << "Invalid file\n";
		return false;
	}
	if(((fileheader.bfType&0x00FF)!='B'||((fileheader.bfType>>8)&0x00FF)!='M'))
	{
		std::cout << "Invalid BMP file\n";
		return false;
	}
	width = infoheader.biWidth;
	height = infoheader.biHeight;
	fseek(f,fileheader.bfOffBits,0);
	texture = (unsigned char *) malloc(infoheader.biWidth * infoheader.biHeight * 4);
	int j=0;
	for (int i=0; i < infoheader.biWidth*infoheader.biHeight; i++)
	{
		fread(&pixel,sizeof(BMPCOLOR),1,f);
		texture[j] = pixel.red;
		texture[j+1] = pixel.green;
		texture[j+2] = pixel.blue;
		texture[j+3] = 255;
		j+=4;
	}
	fclose(f);
	return true;
}

bool BMPTexture::loadToVRAM()
{
	if(load() == false) return false;
	glBindTexture(GL_TEXTURE_2D,0); // Bind the ID texture specified by the 2nd parameter
	// The next commands sets the texture parameters
	// If the u,v coordinates overflow the range 0,1 the image is repeated
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT); 
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT);
	// The magnification function ("linear" produces better results)
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
	//The minifying function
	glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST);
	// We don't combine the color with the original surface color, use only the texture map.
	glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE);

	// Finally we define the 2d texture
	glTexImage2D(GL_TEXTURE_2D,0,4,getWidth(),getHeight(),0,GL_RGBA,GL_UNSIGNED_BYTE,data());

	// And create 2d mipmaps for the minifying function
	gluBuild2DMipmaps(GL_TEXTURE_2D,4,getWidth(),getHeight(),GL_RGBA,GL_UNSIGNED_BYTE,data());
	return true;
}
