#ifndef  _MATRIX_4x4_
#define  _MATRIX_4x4_

#include "String.h"

namespace Engine
{
	template <typename type> class Vector4;
	
	template <typename type> class Matrix4
	{
		private:
			type matrix[4][4];
		public:
			Matrix4();
			Matrix4(type a00, type a01, type a02, type a03,
				 	type a10, type a11, type a12, type a13,
				 	type a20, type a21, type a22, type a23,
					type a30, type a31, type a32, type a33);
			Matrix4(const Vector4<type> &v1,
					const Vector4<type> &v2,
					const Vector4<type> &v3,
					const Vector4<type> &v4);
			~Matrix4();
			
			Matrix4& operator=(const Matrix4 &a);
			Matrix4 operator*(type scalar) const;
			Matrix4 operator/(type scalar) const;
			Matrix4 operator*(const Matrix4 &a) const;
			Matrix4 operator/(const Matrix4 &a) const;
			Matrix4 operator+(const Matrix4 &a) const;
			Matrix4 operator-(const Matrix4 &a) const;
			bool operator==(const Matrix4 &a) const;
			bool operator!=(const Matrix4 &a) const;
			Vector4<type>& operator[](int row);
			
			static Matrix4 identity();
			Matrix4 transpose() const;
			Matrix4 adjoint() const;
			Matrix4 inverse() const;
			type determinant() const;
			Vector4<type> getRow(int row) const;
			Vector4<type> getColumn(int col) const;
			Vector4<type> getDiag() const;
			void setRow(int row, const Vector4<type> &v);
			void setColumn(int col, const Vector4<type> &v);
			void setDiag(const Vector4<type> &v);
			
			String toString() const;
	};
	
	typedef Matrix4<float> 	Matrix4f;
	typedef Matrix4<double> Matrix4d;
}

#endif
