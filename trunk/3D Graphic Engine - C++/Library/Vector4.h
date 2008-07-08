#ifndef  _VECTOR_4D
#define  _VECTOR_4D

#include "String.h"

namespace Engine
{
	template <typename type> class Vector4
	{
		public:
			union
			{ 
				struct { type x,y,z,w; };
				struct { type r,g,b,a; };
			};
		public:
			Vector4();
			Vector4(type x, type y, type z, type w);
			~Vector4();
			
			Vector4& operator=(const Vector4 &vector);
			Vector4 operator+(const Vector4 &vector) const;
			Vector4 operator-(const Vector4 &vector) const;
			Vector4 operator-() const;
			Vector4 operator*(type scalar) const;
			Vector4 operator/(type scalar) const;
			Vector4 operator*(const Vector4 &vector) const;
			Vector4 operator/(const Vector4 &vector) const;
			bool operator==(const Vector4 &vector) const;
			bool operator!=(const Vector4 &vector) const;
			type& operator[](int poz);
			
			type length() const;
			type distance(const Vector4 &other) const;
			Vector4 crossProduct(const Vector4 &vector) const;
			type dotProduct(const Vector4 &vector) const;
			void normalize();
			
			String toString() const;
	};
	
	typedef Vector4<float> 				Vector4f;
	typedef Vector4<double> 			Vector4d;
	typedef Vector4<int> 				Vector4i;
	typedef Vector4<unsigned char> 		Vector4c;
	typedef Vector4<unsigned short> 	Vector4h;
}

#endif
