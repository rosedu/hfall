#include "Matrix3.h"
#include "Vector3.h" 
#include <string.h>
#include <sstream>
#include <stdio.h>

using namespace Engine;

template <typename type> Matrix3<type>::Matrix3()
{
		memset(matrix,0,9*sizeof(type));
}
template <typename type> Matrix3<type>::Matrix3(type a00, type a01, type a02,
				 								type a10, type a11, type a12,
				 								type a20, type a21, type a22)
{
	matrix[0][0] = a00; matrix[0][1] = a01; matrix[0][2] = a02;
	matrix[1][0] = a10; matrix[1][1] = a11; matrix[1][2] = a12;
	matrix[2][0] = a20; matrix[2][1] = a21; matrix[2][2] = a22;
}
template <typename type> Matrix3<type>::Matrix3(const Vector3<type> &v1,
				 								const Vector3<type> &v2,
				 								const Vector3<type> &v3)
{
	memcpy(matrix[0],(void *)&v1,3*sizeof(type));
	memcpy(matrix[1],(void *)&v2,3*sizeof(type));
	memcpy(matrix[2],(void *)&v3,3*sizeof(type));
}					 
template <typename type> Matrix3<type>::~Matrix3() {}


template <typename type> Matrix3<type>& Matrix3<type>::operator=(const Matrix3<type> &a)
{
	memcpy(this,(void *)&a,9*sizeof(type));
	return *this;
}
template <typename type> Vector3<type>& Matrix3<type>::operator[](int row)
{
	if(row < 0 || row > 2) { printf("error: bad Matrix3 index"); exit(0); }
	return ((Vector3<type> *)matrix)[row];
}
template <typename type> Matrix3<type> Matrix3<type>::operator*(type x) const
{
	Matrix3<type> t;
	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
			t.matrix[i][j] = x*matrix[i][j];
	return t;
}
template <typename type> Matrix3<type> Matrix3<type>::operator/(type x) const
{
	Matrix3<type> t;
	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
			t.matrix[i][j] = matrix[i][j]/x;
	return t;
}
template <typename type> Matrix3<type> Matrix3<type>::operator*(const Matrix3<type> &b) const
{
	Matrix3<type> c;
	for(int i=0; i<3; i++)
		for(int j=0; j<3; j++)
		{
			type s=0;
			for(int k=0; k<3; k++)
				s+= matrix[i][k]*b.matrix[k][j];
			c.matrix[i][j] = s;
		}
	return c;
}
template <typename type> Matrix3<type> Matrix3<type>::operator+(const Matrix3<type> &a) const
{
	Matrix3<type> t;
	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
			t.matrix[i][j] = matrix[i][j]+a.matrix[i][j];
	return t;
}
template <typename type> Matrix3<type> Matrix3<type>::operator-(const Matrix3<type> &a) const
{
	Matrix3<type> t;
	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
			t.matrix[i][j] = matrix[i][j]-a.matrix[i][j];
	return t;
}
template <typename type> bool Matrix3<type>::operator==(const Matrix3<type> &a) const
{
	if(memcmp(matrix,a.matrix,9*sizeof(type)) == 0) return true;
	return false;
}
template <typename type> bool Matrix3<type>::operator!=(const Matrix3<type> &a) const
{
	if(memcmp(matrix,a.matrix,9*sizeof(type)) != 0) return true;
	return false;
}

template <typename type> Matrix3<type> Matrix3<type>::identity()
{
	return Matrix3<type>(1,0,0,
				   		 0,1,0,
				   		 0,0,1);
}
template <typename type> Matrix3<type> Matrix3<type>::transpose() const
{
	Matrix3<type> t;
	for(int i=0;i<3;i++)
		for(int j=0;j<3;j++)
			t.matrix[i][j] = matrix[j][i];
	return t;
}
template <typename type> type Matrix3<type>::determinant() const
{
	return matrix[0][0]*matrix[1][1]*matrix[2][2] + matrix[0][1]*matrix[1][2]*matrix[2][0]+
	matrix[0][2]*matrix[1][0]*matrix[2][1] - matrix[0][0]*matrix[1][2]*matrix[2][1] -
	matrix[0][1]*matrix[1][0]*matrix[2][2] - matrix[0][2]*matrix[1][1]*matrix[2][0];
}
template <typename type> Matrix3<type> Matrix3<type>::adjoint() const
{
	return Matrix3<type>(matrix[1][1]*matrix[2][2] - matrix[1][2]*matrix[2][1],
				 	   - matrix[0][1]*matrix[2][2] + matrix[0][2]*matrix[2][1],
				   		 matrix[0][1]*matrix[1][2] - matrix[0][2]*matrix[1][1],
				 	   - matrix[1][0]*matrix[2][2] + matrix[1][2]*matrix[2][0],
				   		 matrix[0][0]*matrix[2][2] - matrix[0][2]*matrix[2][0],
				 	   - matrix[0][0]*matrix[1][2] + matrix[0][2]*matrix[1][0],
				   		 matrix[1][0]*matrix[2][1] - matrix[1][1]*matrix[2][0],
				 	   - matrix[0][0]*matrix[2][1] + matrix[0][1]*matrix[2][0],
				   		 matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]);
}
template <typename type> Matrix3<type> Matrix3<type>::inverse() const
{
	return adjoint()/determinant();
}
template <typename type> void Matrix3<type>::orthonormalize()
{
	double inv_length = 1/sqrt(matrix[0][0]*matrix[0][0] +
	matrix[1][0]*matrix[1][0] + matrix[2][0]*matrix[2][0]);
	matrix[0][0] = (type)(matrix[0][0] * inv_length);
	matrix[1][0] = (type)(matrix[1][0] * inv_length);
	matrix[2][0] = (type)(matrix[2][0] * inv_length);
	
	matrix[0][2] = matrix[1][0]*matrix[2][1] - matrix[2][0]*matrix[1][1];
	matrix[1][2] = matrix[2][0]*matrix[0][1] - matrix[0][0]*matrix[2][1];
	matrix[2][2] = matrix[0][0]*matrix[1][1] - matrix[1][0]*matrix[0][1];
	inv_length = 1/sqrt(matrix[0][2]*matrix[0][2] +
	matrix[1][2]*matrix[1][2] + matrix[2][2]*matrix[2][2]);
	matrix[0][2] = (type)(matrix[0][2] * inv_length);
	matrix[1][2] = (type)(matrix[1][2] * inv_length);
	matrix[2][2] = (type)(matrix[2][2] * inv_length);
	
	matrix[0][1] = matrix[1][2]*matrix[2][0] - matrix[2][2]*matrix[1][0];
	matrix[1][1] = matrix[2][2]*matrix[0][0] - matrix[0][2]*matrix[2][0];
	matrix[2][1] = matrix[0][2]*matrix[1][0] - matrix[1][2]*matrix[0][0];
	inv_length = 1/sqrt(matrix[0][1]*matrix[0][1] +
	matrix[1][1]*matrix[1][1] + matrix[2][1]*matrix[2][1]);
	matrix[0][1] = (type)(matrix[0][1] * inv_length);
	matrix[1][1] = (type)(matrix[1][1] * inv_length);
	matrix[2][1] = (type)(matrix[2][1] * inv_length);
}
template <typename type> Vector3<type> Matrix3<type>::getRow(int row) const
{
	if(row < 0 || row > 2) { printf("error: bad Matrix3 index"); exit(0); }
	return Vector3<type>(matrix[row][0],matrix[row][1],matrix[row][2]);
}
template <typename type> Vector3<type> Matrix3<type>::getColumn(int col) const
{
	if(row < 0 || row > 2) { printf("error: bad Matrix3 index"); exit(0); }
	return Vector3<type>(matrix[0][col],matrix[1][col],matrix[2][col]);
}
template <typename type> Vector3<type> Matrix3<type>::getDiag() const
{
	return Vector3<type>(matrix[0][0],matrix[1][1],matrix[2][2]);
}
template <typename type> void Matrix3<type>::setRow(int row, const Vector3<type> &v)
{
	if(row < 0 || row > 2) { printf("error: bad Matrix3 index"); exit(0); }
	matrix[row][0] = v.x;
	matrix[row][1] = v.y;
	matrix[row][2] = v.z;
}
template <typename type> void Matrix3<type>::setColumn(int col, const Vector3<type> &v)
{
	if(row < 0 || row > 2) { printf("error: bad Matrix3 index"); exit(0); }
	matrix[0][col] = v.x;
	matrix[1][col] = v.y;
	matrix[2][col] = v.z;
}
template <typename type> void Matrix3<type>::setDiag(const Vector3<type> &v)
{
	matrix[0][0] = v.x;
	matrix[1][1] = v.y;
	matrix[2][2] = v.z;
}

template <typename type> String Matrix3<type>::toString() const
{
	std::stringstream out;
	out << matrix[0][0] << " " << matrix[0][1] << " " << matrix[0][2] << " " << "\n";
	out << matrix[1][0] << " " << matrix[1][1] << " " << matrix[1][2] << " " << "\n";
	out << matrix[2][0] << " " << matrix[2][1] << " " << matrix[2][2] << " " << "\n";
	return out.str();
}

template Matrix3<float>;
template Matrix3<double>;
