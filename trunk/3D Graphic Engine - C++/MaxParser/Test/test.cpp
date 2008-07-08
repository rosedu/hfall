#include "MaxParser.h"
#include <stdio.h>
#include <string.h>


int main(int args, char *argc[])
{
	if(args < 2 || args > 3)
	{
		printf("Invalid argument");
		exit(0);
	}
	
	MaxParser p(argc[1]);
	p.parse(true,false);
	
	return 0;
}
