#include "Vector4.h"
#include <math.h>
#include <sstream>
#include <stdio.h>

using namespace Engine;

template <typename type> Vector4<type>::Vector4() { x = y = z = w = 0; }
template <typename type> Vector4<type>::Vector4(type xx, type yy, type zz, type ww)
{
	x = xx;
	y = yy;
	z = zz;
	w = ww;
}
template <typename type> Vector4<type>::~Vector4() {}


template <typename type> Vector4<type>& Vector4<type>::operator=(const Vector4<type> &vector)
{
	memcpy(this,(void *)&vector,4*sizeof(type));
	return *this;
}
template <typename type> Vector4<type> Vector4<type>::operator+(const Vector4<type> &a) const
{
	return Vector4<type>(x+a.x,y+a.y,z+a.z,w+a.w);
}
template <typename type> Vector4<type> Vector4<type>::operator-(const Vector4<type> &a) const
{
	return Vector4<type>(x-a.x,y-a.y,z-a.z,w-a.w);
}
template <typename type> Vector4<type> Vector4<type>::operator-() const
{
	return Vector4<type>(-x,-y,-z,-w);
}
template <typename type> Vector4<type> Vector4<type>::operator*(type c) const
{
	return Vector4<type>(x*c,y*c,z*c,w*c);
}
template <typename type> Vector4<type> Vector4<type>::operator/(type c) const
{
	return Vector4<type>(x/c,y/c,z/c,w/c);
}
template <typename type> Vector4<type> Vector4<type>::operator*(const Vector4<type> &a) const
{
	return Vector4<type>(x*a.x,y*a.y,z*a.z,w*a.w);
}
template <typename type> Vector4<type> Vector4<type>::operator/(const Vector4<type> &a) const
{
	return Vector4<type>(x/a.x,y/a.y,z/a.z,w/a.w);
}
template <typename type> bool Vector4<type>::operator ==(const Vector4<type> &a) const
{
	return x == a.x && y == a.y && z == a.z && w == a.w;
}
template <typename type> bool Vector4<type>::operator !=(const Vector4<type> &a) const
{
	return x != a.x || y != a.y || z != a.z || w != a.w;
}
template <typename type> type& Vector4<type>::operator[](int i)
{
	if(i<0 || i>3) { printf("error: bad Vector4 index"); exit(0); }
	return ((type *)this)[i];
}

template <typename type> type Vector4<type>::length() const
{
	return (type)sqrt(x*x + y*y + z*z + w*w);
}
template <typename type> Vector4<type> Vector4<type>::crossProduct(const Vector4<type> &a) const
{
	return Vector4<type>(y*a.z - z*a.y,
				   		 z*a.x - x*a.z,
				   		 x*a.y - y*a.x,
				   		 0);
}
template <typename type> type Vector4<type>::dotProduct(const Vector4<type> &a) const
{
	return x*a.x + y*a.y + z*a.z + w*a.w;
}
template <typename type> void Vector4<type>::normalize()
{
	double inv_length = 1/sqrt(x*x + y*y + z*z + w*w);
	x = (type)(x * inv_length);
	y = (type)(y * inv_length);
	z = (type)(z * inv_length);
	w = (type)(w * inv_length);
}


template <typename type> String Vector4<type>::toString() const
{
	std::stringstream out;
	out << "[" << x << " " << y << " " << z << " " << w << "]";
	return out.str();
}

template Vector4<float>;
template Vector4<double>;
template Vector4<int>;
template Vector4<unsigned char>;
template Vector4<unsigned short>;
