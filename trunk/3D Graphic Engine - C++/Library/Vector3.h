#ifndef  _VECTOR_3D
#define  _VECTOR_3D

#include "String.h"

namespace Engine
{	
	template <typename type> class Vector3
	{
		public:
			union
			{ 
				struct { type x,y,z; };
				struct { type r,g,b; };
			};
		public:
			Vector3();
			Vector3(type x, type y, type z);
			~Vector3();
			
			Vector3& operator=(const Vector3 &vector);
			Vector3 operator+(const Vector3 &vector) const;
			Vector3 operator-(const Vector3 &vector) const;
			Vector3 operator-() const;
			Vector3 operator*(type scalar) const;
			Vector3 operator/(type scalar) const;
			Vector3 operator*(const Vector3 &vector) const;
			Vector3 operator/(const Vector3 &vector) const;
			bool operator==(const Vector3 &vector) const;
			bool operator!=(const Vector3 &vector) const;
			type& operator[](int poz);
			
			type length() const;
			type distance(const Vector3 &other) const;
			Vector3 crossProduct(const Vector3 &vector) const;
			type dotProduct(const Vector3 &vector) const;
			void normalize();
			
			String toString() const;
	};
	
	typedef Vector3<float> 				Vector3f;
	typedef Vector3<double> 			Vector3d;
	typedef Vector3<int> 				Vector3i;
	typedef Vector3<unsigned char> 		Vector3c;
	typedef Vector3<unsigned short> 	Vector3h;
}

#endif
