#ifndef BITMAP_H_
#define BITMAP_H_

#include <stdint.h>


typedef struct fileheader 
{ 
  uint16_t	bfType; 
  uint32_t	bfSize; 
  uint16_t	bfReserved1; 
  uint16_t	bfReserved2; 
  uint32_t	bfOffBits; 
} __attribute__((__packed__)) BITMAPFILEHEADER;

typedef struct infoheader 
{
  uint32_t	biSize; 
  int32_t	biWidth; 
  int32_t	biHeight; 
  uint16_t	biPlanes; 
  uint16_t	biBitCount; 
  uint32_t	biCompression; 
  uint32_t	biSizeImage; 
  int32_t	biXPelsPerMeter; 
  int32_t	biYPelsPerMeter; 
  uint32_t	biClrUsed; 
  uint32_t	biClrImportant; 
} __attribute__((__packed__)) BITMAPINFOHEADER;

typedef struct color 
{
	uint8_t blue;
	uint8_t green;
	uint8_t red;
} __attribute__((__packed__)) BMPCOLOR;

#define BI_RGB        0L
#define BI_RLE8       1L
#define BI_RLE4       2L
#define BI_BITFIELDS  3L
#define BI_JPEG       4L
#define BI_PNG        5L


#endif
