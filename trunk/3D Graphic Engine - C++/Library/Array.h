#ifndef __ARRAY__
#define __ARRAY__


template <class type> class Array
{
	public:
		Array();
		Array(int size);
		void clear();
		type& operator[](int pos);
		void add(const type &value);
		int size() { return _size; }
		type *getData();
		
	private:
		type *data;
		int _size;
		int max_size;
};

/* ########################################################################
						     Implementation
   ######################################################################## */

#include <stdlib.h>

template <class type> Array<type>::Array()
{
	_size = 0;
	max_size = 0;
	data = NULL;
}
template <class type> Array<type>::Array(int s)
{
	_size = 0;
	max_size = s;
	data = (type *)malloc(max_size*sizeof(type));
}
template <class type> void Array<type>::clear()
{
	free(data);
	data = NULL;
	_size = max_size = 0;
}
template <class type> type& Array<type>::operator[](int i)
{
	if(i<0 || i>=_size) exit(0);
	return data[i];
}
template <class type> void Array<type>::add(const type &d)
{
	if(_size == max_size)
	{
		max_size+= 5;
		data = (type *)realloc(data,max_size*sizeof(type));
	}
	data[_size++] = d;
}
template <class type> type *Array<type>::getData()
{
	data = (type *)realloc(data,_size*sizeof(type));
	return data;
}

#endif
