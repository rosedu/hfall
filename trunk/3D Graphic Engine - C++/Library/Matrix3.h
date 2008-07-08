#ifndef  _MATRIX_3x3_
#define  _MATRIX_3x3_

#include "String.h"

namespace Engine
{
	template <typename type> class Vector3;
	
	template <typename type> class Matrix3
	{
		private:
			type matrix[3][3];
		public:
			Matrix3();
			Matrix3(type a00, type a01, type a02,
				 	type a10, type a11, type a12,
				 	type a20, type a21, type a22);
			Matrix3(const Vector3<type> &v1,
					const Vector3<type> &v2,
					const Vector3<type> &v3);
			~Matrix3();
			
			Matrix3& operator=(const Matrix3 &a);
			Matrix3 operator*(type scalar) const;
			Matrix3 operator/(type scalar) const;
			Matrix3 operator*(const Matrix3 &a) const;
			Matrix3 operator/(const Matrix3 &a) const;
			Matrix3 operator+(const Matrix3 &a) const;
			Matrix3 operator-(const Matrix3 &a) const;
			bool operator==(const Matrix3 &a) const;
			bool operator!=(const Matrix3 &a) const;
			Vector3<type>& operator[](int row);
			
			static Matrix3 identity();
			Matrix3 transpose() const;
			Matrix3 adjoint() const;
			Matrix3 inverse() const;
			void orthonormalize();
			type determinant() const;
			Vector3<type> getRow(int row) const;
			Vector3<type> getColumn(int col) const;
			Vector3<type> getDiag() const;
			void setRow(int row, const Vector3<type> &v);
			void setColumn(int col, const Vector3<type> &v);
			void setDiag(const Vector3<type> &v);
			
			String toString() const;
	};
	
	typedef Matrix3<float> 	Matrix3f;
	typedef Matrix3<double> Matrix3d;
}

#endif
