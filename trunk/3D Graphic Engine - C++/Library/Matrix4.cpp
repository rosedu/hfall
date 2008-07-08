#include "Matrix4.h"
#include "Vector4.h"
#include <string.h>
#include <sstream>
#include <stdio.h>

using namespace Engine;

template <typename type> Matrix4<type>::Matrix4()
{
		memset(matrix,0,16*sizeof(type));
}
template <typename type> Matrix4<type>::Matrix4(type a00, type a01, type a02, type a03,
				 								type a10, type a11, type a12, type a13,
				 								type a20, type a21, type a22, type a23,
				 								type a30, type a31, type a32, type a33)
{
	matrix[0][0] = a00; matrix[0][1] = a01; matrix[0][2] = a02; matrix[0][3] = a03;
	matrix[1][0] = a10; matrix[1][1] = a11; matrix[1][2] = a12; matrix[1][3] = a13;
	matrix[2][0] = a20; matrix[2][1] = a21; matrix[2][2] = a22; matrix[2][3] = a23;
	matrix[3][0] = a30; matrix[3][1] = a31; matrix[3][2] = a32; matrix[3][3] = a33;
}
template <typename type> Matrix4<type>::Matrix4(const Vector4<type> &v1,
				 								const Vector4<type> &v2,
				 								const Vector4<type> &v3,
				 								const Vector4<type> &v4)
{
	memcpy(matrix[0],(void *)&v1,4*sizeof(type));
	memcpy(matrix[1],(void *)&v2,4*sizeof(type));
	memcpy(matrix[2],(void *)&v3,4*sizeof(type));
	memcpy(matrix[3],(void *)&v3,4*sizeof(type));
}
template <typename type> Matrix4<type>::~Matrix4() {}


template <typename type> Matrix4<type>& Matrix4<type>::operator=(const Matrix4<type> &a)
{
	memcpy(this,(void *)&a,16*sizeof(type));
	return *this;
}
template <typename type> Vector4<type>& Matrix4<type>::operator[](int row)
{
	if(row < 0 || row > 3) { printf("error: bad Matrix4 index"); exit(0); }
	return ((Vector4<type> *)matrix)[row];
}
template <typename type> Matrix4<type> Matrix4<type>::operator*(type x) const
{
	Matrix4<type> t;
	for(int i=0;i<4;i++)
		for(int j=0;j<4;j++)
			t.matrix[i][j] = x*matrix[i][j];
	return t;
}
template <typename type> Matrix4<type> Matrix4<type>::operator/(type x) const
{
	Matrix4<type> t;
	for(int i=0;i<4;i++)
		for(int j=0;j<4;j++)
			t.matrix[i][j] = matrix[i][j]/x;
	return t;
}
template <typename type> Matrix4<type> Matrix4<type>::operator*(const Matrix4<type> &b) const
{
	Matrix4<type> c;
	for(int i=0; i<4; i++)
		for(int j=0; j<4; j++)
		{
			type s=0;
			for(int k=0; k<4; k++)
				s+= matrix[i][k]*b.matrix[k][j];
			c[i][j] = s;
		}
	return c;
}
template <typename type> Matrix4<type> Matrix4<type>::operator+(const Matrix4<type> &a) const
{
	Matrix4<type> t;
	for(int i=0;i<4;i++)
		for(int j=0;j<4;j++)
			t.matrix[i][j] = matrix[i][j]+a.matrix[i][j];
	return t;
}
template <typename type> Matrix4<type> Matrix4<type>::operator-(const Matrix4<type> &a) const
{
	Matrix4<type> t;
	for(int i=0;i<4;i++)
		for(int j=0;j<4;j++)
			t.matrix[i][j] = matrix[i][j]-a.matrix[i][j];
	return t;
}
template <typename type> bool Matrix4<type>::operator==(const Matrix4<type> &a) const
{
	if(memcmp(matrix,a.matrix,16*sizeof(type)) == 0) return true;
	return false;
}
template <typename type> bool Matrix4<type>::operator!=(const Matrix4<type> &a) const
{
	if(memcmp(matrix,a.matrix,16*sizeof(type)) != 0) return true;
	return false;
}

template <typename type> Matrix4<type> Matrix4<type>::identity()
{
	return Matrix4<type>(1,0,0,0,
				   		 0,1,0,0,
				   		 0,0,1,0,
				   		 0,0,0,1);
}
template <typename type> Matrix4<type> Matrix4<type>::transpose() const
{
	Matrix4<type> t;
	for(int i=0;i<4;i++)
		for(int j=0;j<4;j++)
			t.matrix[i][j] = matrix[j][i];
	return t;
}
template <typename type> type Matrix4<type>::determinant() const
{
	type *s = (type *) malloc(6*sizeof(type));
	s[0] = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0];
	s[1] = matrix[0][0]*matrix[1][2] - matrix[0][2]*matrix[1][0];
	s[2] = matrix[0][0]*matrix[1][3] - matrix[0][3]*matrix[1][0];
	s[3] = matrix[0][1]*matrix[1][2] - matrix[0][2]*matrix[1][1];
	s[4] = matrix[0][1]*matrix[1][3] - matrix[0][3]*matrix[1][1];
	s[5] = matrix[0][2]*matrix[1][3] - matrix[0][3]*matrix[1][2];
	type *c = (type *) malloc(6*sizeof(type));
	c[0] = matrix[2][2]*matrix[3][3] - matrix[2][3]*matrix[3][2];
	c[1] = matrix[2][1]*matrix[3][3] - matrix[2][3]*matrix[3][1];
	c[2] = matrix[2][1]*matrix[3][2] - matrix[2][2]*matrix[3][1];
	c[3] = matrix[2][0]*matrix[3][3] - matrix[2][3]*matrix[3][0];
	c[4] = matrix[2][0]*matrix[3][2] - matrix[2][2]*matrix[3][0];
	c[5] = matrix[2][0]*matrix[3][1] - matrix[2][1]*matrix[3][0];
	return s[0]*c[0] - s[1]*c[1] + s[2]*c[2] + s[3]*c[3] - s[4]*c[4] + s[5]*c[5];
}
template <typename type> Matrix4<type> Matrix4<type>::adjoint() const
{
	type *s = (type *) malloc(6*sizeof(type));
	s[0] = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0];
	s[1] = matrix[0][0]*matrix[1][2] - matrix[0][2]*matrix[1][0];
	s[2] = matrix[0][0]*matrix[1][3] - matrix[0][3]*matrix[1][0];
	s[3] = matrix[0][1]*matrix[1][2] - matrix[0][2]*matrix[1][1];
	s[4] = matrix[0][1]*matrix[1][3] - matrix[0][3]*matrix[1][1];
	s[5] = matrix[0][2]*matrix[1][3] - matrix[0][3]*matrix[1][2];
	type *c = (type *) malloc(6*sizeof(type));
	c[0] = matrix[2][2]*matrix[3][3] - matrix[2][3]*matrix[3][2];
	c[1] = matrix[2][1]*matrix[3][3] - matrix[2][3]*matrix[3][1];
	c[2] = matrix[2][1]*matrix[3][2] - matrix[2][2]*matrix[3][1];
	c[3] = matrix[2][0]*matrix[3][3] - matrix[2][3]*matrix[3][0];
	c[4] = matrix[2][0]*matrix[3][2] - matrix[2][2]*matrix[3][0];
	c[5] = matrix[2][0]*matrix[3][1] - matrix[2][1]*matrix[3][0];
	return Matrix4<type>(matrix[1][1]*c[0] - matrix[1][2]*c[1] + matrix[1][3]*c[2],
				 	   - matrix[0][1]*c[0] + matrix[0][2]*c[1] - matrix[0][3]*c[2],
				   		 matrix[3][1]*s[5] - matrix[3][2]*s[4] + matrix[3][3]*s[3],
				 	   - matrix[2][1]*s[5] + matrix[2][2]*s[4] - matrix[2][3]*s[3],
				 	   - matrix[1][0]*c[0] + matrix[1][2]*c[3] - matrix[1][3]*c[4],
				   		 matrix[0][0]*c[0] - matrix[0][2]*c[3] + matrix[0][3]*c[4],
				 	   - matrix[3][0]*s[5] + matrix[3][2]*s[2] - matrix[3][3]*s[1],
				  		 matrix[2][0]*s[5] - matrix[2][2]*s[2] + matrix[2][3]*s[1],
				   		 matrix[1][0]*c[1] - matrix[1][1]*c[3] + matrix[1][3]*c[5],
				 	   - matrix[0][0]*c[1] + matrix[0][1]*c[3] - matrix[0][3]*c[5],
				  		 matrix[3][0]*s[4] - matrix[3][1]*s[2] + matrix[3][3]*s[0],
				 	   - matrix[2][0]*s[4] + matrix[2][1]*s[2] - matrix[2][3]*s[0],
				 	   - matrix[1][0]*c[2] + matrix[1][1]*c[4] - matrix[1][2]*c[5],
				 		 matrix[0][0]*c[2] - matrix[0][1]*c[4] + matrix[0][2]*c[5],
				 	   - matrix[3][0]*s[3] + matrix[3][1]*s[1] - matrix[3][2]*s[0],
				  		 matrix[2][0]*s[3] - matrix[2][1]*s[1] + matrix[2][2]*s[0]);
}
template <typename type> Matrix4<type> Matrix4<type>::inverse() const
{
	type *s = (type *) malloc(6*sizeof(type));
	s[0] = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0];
	s[1] = matrix[0][0]*matrix[1][2] - matrix[0][2]*matrix[1][0];
	s[2] = matrix[0][0]*matrix[1][3] - matrix[0][3]*matrix[1][0];
	s[3] = matrix[0][1]*matrix[1][2] - matrix[0][2]*matrix[1][1];
	s[4] = matrix[0][1]*matrix[1][3] - matrix[0][3]*matrix[1][1];
	s[5] = matrix[0][2]*matrix[1][3] - matrix[0][3]*matrix[1][2];
	type *c = (type *) malloc(6*sizeof(type));
	c[0] = matrix[2][2]*matrix[3][3] - matrix[2][3]*matrix[3][2];
	c[1] = matrix[2][1]*matrix[3][3] - matrix[2][3]*matrix[3][1];
	c[2] = matrix[2][1]*matrix[3][2] - matrix[2][2]*matrix[3][1];
	c[3] = matrix[2][0]*matrix[3][3] - matrix[2][3]*matrix[3][0];
	c[4] = matrix[2][0]*matrix[3][2] - matrix[2][2]*matrix[3][0];
	c[5] = matrix[2][0]*matrix[3][1] - matrix[2][1]*matrix[3][0];
	type det = s[0]*c[0] - s[1]*c[1] + s[2]*c[2] + s[3]*c[3] - s[4]*c[4] + s[5]*c[5];
	if(det == 0) return Matrix4<type>();
	return Matrix4<type>((matrix[1][1]*c[0] - matrix[1][2]*c[1] + matrix[1][3]*c[2])/det,
				 	   (- matrix[0][1]*c[0] + matrix[0][2]*c[1] - matrix[0][3]*c[2])/det,
		   		   		 (matrix[3][1]*s[5] - matrix[3][2]*s[4] + matrix[3][3]*s[3])/det,
				 	   (- matrix[2][1]*s[5] + matrix[2][2]*s[4] - matrix[2][3]*s[3])/det,
				 	   (- matrix[1][0]*c[0] + matrix[1][2]*c[3] - matrix[1][3]*c[4])/det,
				   		 (matrix[0][0]*c[0] - matrix[0][2]*c[3] + matrix[0][3]*c[4])/det,
				 	   (- matrix[3][0]*s[5] + matrix[3][2]*s[2] - matrix[3][3]*s[1])/det,
				   		 (matrix[2][0]*s[5] - matrix[2][2]*s[2] + matrix[2][3]*s[1])/det,
				   		 (matrix[1][0]*c[1] - matrix[1][1]*c[3] + matrix[1][3]*c[5])/det,
				 	   (- matrix[0][0]*c[1] + matrix[0][1]*c[3] - matrix[0][3]*c[5])/det,
				   		 (matrix[3][0]*s[4] - matrix[3][1]*s[2] + matrix[3][3]*s[0])/det,
				 	   (- matrix[2][0]*s[4] + matrix[2][1]*s[2] - matrix[2][3]*s[0])/det,
				 	   (- matrix[1][0]*c[2] + matrix[1][1]*c[4] - matrix[1][2]*c[5])/det,
				   		 (matrix[0][0]*c[2] - matrix[0][1]*c[4] + matrix[0][2]*c[5])/det,
				 	   (- matrix[3][0]*s[3] + matrix[3][1]*s[1] - matrix[3][2]*s[0])/det,
				   		 (matrix[2][0]*s[3] - matrix[2][1]*s[1] + matrix[2][2]*s[0])/det);
}
template <typename type> Vector4<type> Matrix4<type>::getRow(int row) const
{
	if(row < 0 || row > 3) { printf("error: bad Matrix4 index"); exit(0); }
	return Vector4<type>(matrix[row][0],matrix[row][1],matrix[row][2],matrix[row][3]);
}
template <typename type> Vector4<type> Matrix4<type>::getColumn(int col) const
{
	if(row < 0 || row > 3) { printf("error: bad Matrix4 index"); exit(0); }
	return Vector4<type>(matrix[0][col],matrix[1][col],matrix[2][col],matrix[3][col]);
}
template <typename type> Vector4<type> Matrix4<type>::getDiag() const
{
	return Vector4<type>(matrix[0][0],matrix[1][1],matrix[2][2],matrix[3][3]);
}
template <typename type> void Matrix4<type>::setRow(int row, const Vector4<type> &v)
{
	if(row < 0 || row > 3) { printf("error: bad Matrix4 index"); exit(0); }
	matrix[row][0] = v.x;
	matrix[row][1] = v.y;
	matrix[row][2] = v.z;
	matrix[row][3] = v.w;
}
template <typename type> void Matrix4<type>::setColumn(int col, const Vector4<type> &v)
{
	if(row < 0 || row > 3) { printf("error: bad Matrix4 index"); exit(0); }
	matrix[0][col] = v.x;
	matrix[1][col] = v.y;
	matrix[2][col] = v.z;
	matrix[3][col] = v.w;
}
template <typename type> void Matrix4<type>::setDiag(const Vector4<type> &v)
{
	matrix[0][0] = v.x;
	matrix[1][1] = v.y;
	matrix[2][2] = v.z;
	matrix[3][3] = v.w;
}


template <typename type> String Matrix4<type>::toString() const
{
	std::stringstream out;
	out << matrix[0][0] << " " << matrix[0][1] << " " << matrix[0][2] << " " << matrix[0][3] << "\n";
	out << matrix[1][0] << " " << matrix[1][1] << " " << matrix[1][2] << " " << matrix[1][3] << "\n";
	out << matrix[2][0] << " " << matrix[2][1] << " " << matrix[2][2] << " " << matrix[2][3] << "\n";
	out << matrix[3][0] << " " << matrix[3][1] << " " << matrix[3][2] << " " << matrix[3][3] << "\n";
	return out.str();
}

template Matrix4<float>;
template Matrix4<double>;
