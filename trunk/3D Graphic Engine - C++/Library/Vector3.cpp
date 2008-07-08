#include "Vector3.h"
#include <math.h>
#include <sstream>
#include <stdio.h>

using namespace Engine;

template <typename type> Vector3<type>::Vector3() { x=0; y=0; z=0; }
template <typename type> Vector3<type>::Vector3(type xx, type yy, type zz)
{
	x = xx;
	y = yy;
	z = zz;
}
template <typename type> Vector3<type>::~Vector3() {}


template <typename type> Vector3<type>& Vector3<type>::operator=(const Vector3<type> &vector)
{
	memcpy(this,(void *)&vector,3*sizeof(type));
	return *this;
}
template <typename type> Vector3<type> Vector3<type>::operator+(const Vector3<type> &a) const
{
	return Vector3<type>(x+a.x,y+a.y,z+a.z);
}
template <typename type> Vector3<type> Vector3<type>::operator-(const Vector3<type> &a) const
{
	return Vector3<type>(x-a.x,y-a.y,z-a.z);
}
template <typename type> Vector3<type> Vector3<type>::operator-() const
{
	return Vector3<type>(-x,-y,-z);
}
template <typename type> Vector3<type> Vector3<type>::operator*(type c) const
{
	return Vector3<type>(x*c,y*c,z*c);
}
template <typename type> Vector3<type> Vector3<type>::operator/(type c) const
{
	return Vector3<type>(x/c,y/c,z/c);
}
template <typename type> Vector3<type> Vector3<type>::operator*(const Vector3<type> &a) const
{
	return Vector3<type>(x*a.x,y*a.y,z*a.z);
}
template <typename type> Vector3<type> Vector3<type>::operator/(const Vector3<type> &a) const
{
	return Vector3<type>(x/a.x,y/a.y,z/a.z);
}
template <typename type> bool Vector3<type>::operator ==(const Vector3<type> &a) const
{
	return x == a.x && y == a.y && z == a.z;
}
template <typename type> bool Vector3<type>::operator !=(const Vector3<type> &a) const
{
	return x != a.x || y != a.y || z != a.z;
}
template <typename type> type& Vector3<type>::operator[](int i)
{
	if(i<0 || i>2) { printf("error: bad Vector3 index"); exit(0); }
	return ((type *)this)[i];
}

template <typename type> type Vector3<type>::length() const
{
	return (type)sqrt((x*x + y*y + z*z));
}
template <typename type> Vector3<type> Vector3<type>::crossProduct(const Vector3<type> &a) const
{
	return Vector3<type>(y*a.z - z*a.y,
				   		 z*a.x - x*a.z,
				   		 x*a.y - y*a.x);
}
template <typename type> type Vector3<type>::dotProduct(const Vector3<type> &a) const
{
	return x*a.x + y*a.y + z*a.z;
}
template <typename type> void Vector3<type>::normalize()
{
	double inv_length = 1/sqrt(x*x + y*y + z*z);
	x = (type)(x * inv_length);
	y = (type)(y * inv_length);
	z = (type)(z * inv_length);
}


template <typename type> String Vector3<type>::toString() const
{
	std::stringstream out;
	out << "[" << x << " " << y << " " << z << "]";
	return out.str();
}

template Vector3<unsigned char>;
template Vector3<unsigned short>;
template Vector3<int>;
template Vector3<float>;
template Vector3<double>;
