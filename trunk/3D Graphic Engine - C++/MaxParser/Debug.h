#ifndef __DEBUG__
#define __DEBUG__

#include <stdio.h>
#include <stdarg.h>

void debugPrintf(const char *fmt ...)
{
	#ifdef DEBUG
		va_list argList;
    	va_start(argList, fmt);
    	vprintf(fmt,argList);
    	va_end(argList);
	#endif
}

#endif
